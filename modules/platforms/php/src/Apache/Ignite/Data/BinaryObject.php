<?php
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

namespace Apache\Ignite\Data;

use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Type\ComplexObjectType;
use Apache\Ignite\Impl\Binary\BinaryTypeBuilder;
use Apache\Ignite\Impl\Binary\BinaryObjectField;
use Apache\Ignite\Impl\Binary\MessageBuffer;
use Apache\Ignite\Impl\Binary\BinaryUtils;
use Apache\Ignite\Impl\Binary\BinaryField;
use Apache\Ignite\Impl\Utils\ArgumentChecker;
use Apache\Ignite\Impl\Utils\Logger;

/**
 * Class representing a complex Ignite object in the binary form.
 *
 * It corresponds to COMPOSITE_TYPE.COMPLEX_OBJECT {@link ObjectType.COMPOSITE_TYPE},
 * has mandatory type Id, which corresponds to a name of the complex type,
 * and includes optional fields.
 *
 * An instance of the BinaryObject can be obtained/created by the following ways:
 *   - returned by the client when a complex object is received from Ignite cache
 * and is not deserialized to another JavaScript object.
 *   - created using the public constructor. Fields may be added to such an instance using setField() method.
 *   - created from a JavaScript object using static fromObject() method.
 */
class BinaryObject
{
    const HEADER_LENGTH = 24;
    const VERSION = 1;

    // user type
    const FLAG_USER_TYPE = 0x0001;
    // schema exists
    const FLAG_HAS_SCHEMA = 0x0002;
    // object contains raw data
    const FLAG_HAS_RAW_DATA = 0x0004;
    // offsets take 1 byte
    const FLAG_OFFSET_ONE_BYTE = 0x0008;
    // offsets take 2 bytes
    const FLAG_OFFSET_TWO_BYTES = 0x0010;
    // compact footer, no field IDs
    const FLAG_COMPACT_FOOTER = 0x0020;
    
    private $typeName;
    private $fields;
    private $typeBuilder;
    private $modified;
    private $buffer;
    private $schemaOffset;
    private $compactFooter;

    /**
     * Creates an instance of the BinaryObject without any fields.
     *
     * Fields may be added later using setField() method.
     *
     * @param string $typeName name of the complex type to generate the type Id.
     *
     * @return BinaryObject new BinaryObject instance.
     *
     * @throws Exception::ClientException if error.
     */
    public function __construct(string $typeName)
    {
        ArgumentChecker::notEmpty($typeName, 'typeName');
        $this->typeName = $typeName;
        $this->fields = [];
        $this->typeBuilder = BinaryTypeBuilder::fromTypeName($typeName);
        $this->modified = false;
        $this->buffer = null;
        $this->schemaOffset = null;
        $this->compactFooter = false;
    }

    /**
     * Creates an instance of the BinaryObject from the specified instance of PHP Object.
     *
     * All public properties of the PHP Object instance with their values are added as fields
     * to the BinaryObject.
     * Fields may be added or removed later using setField() and removeField() methods.
     *
     * If complexObjectType parameter is specified, then the type Id is taken from it.
     * Otherwise, the type Id is generated from the name of the PHP Object.
     * 
     * @param object $object instance of PHP Object which adds and initializes the fields
     *     of the BinaryObject instance.
     * @param ComplexObjectType $complexObjectType instance of complex type definition
     *   which specifies non-standard mapping of the fields of the BinaryObject instance
     *   to/from the Ignite types.
     * 
     * @return BinaryObject new BinaryObject instance.
     * 
     * @throws Exception::ClientException if error.
     */
    public static function fromObject(object $object, ComplexObjectType $complexObjectType = null): BinaryObject
    {
        $typeBuilder = BinaryTypeBuilder::fromObject($object, $complexObjectType);
        $result = new BinaryObject($typeBuilder->getTypeName());
        $result->typeBuilder = $typeBuilder;
        $className = $typeBuilder->getType()->getName();
        try {
            $class = new \ReflectionClass($className);
        } catch (\ReflectionException $e) {
            BinaryUtils::serializationError(true, sprintf('class "%s" does not exist', $className));
        }
        foreach ($typeBuilder->getFields() as $field) {
            $fieldName = $field->getName();
            try {
                if ($class->hasProperty($fieldName)) {
                    $result->setField(
                        $fieldName,
                        $class->getProperty($fieldName)->getValue($object),
                        $complexObjectType ? $complexObjectType->getFieldType($fieldName) : null);
                }
            } catch (\ReflectionException $e) {
                BinaryUtils::serializationError(true, sprintf('field "%s" is undefined', $fieldName));
            }
        }
        return $result;
    }
    
    /**
     * Sets the new value of the specified field.
     * Adds the specified field, if it did not exist before.
     *
     * Optionally, specifies a type of the field.
     * If the type is not specified then during operations the Ignite client
     * will try to make automatic mapping between PHP types and Ignite object types -
     * according to the mapping table defined in the description of the ObjectType class.
     * 
     * @param string $fieldName name of the field.
     * @param mixed $fieldValue new value of the field.
     * @param int|ObjectType|null $fieldType type of the field:
     *   - either a type code of primitive (simple) type (@ref PrimitiveTypeCodes)
     *   - or an instance of class representing non-primitive (composite) type
     *   - or null (or not specified) that means the type is not specified
     * 
     * @return BinaryObject the same instance of BinaryObject.
     * 
     * @throws Exception::ClientException if error.
     */
    public function setField(string $fieldName, $fieldValue, $fieldType = null): BinaryObject
    {
        ArgumentChecker::notEmpty($fieldName, 'fieldName');
        BinaryUtils::checkObjectType($fieldType, 'fieldType');
        $this->modified = true;
        $field = new BinaryObjectField($fieldName, $fieldValue, $fieldType);
        $this->fields[$field->getId()] = $field;
        $this->typeBuilder->setField($fieldName, $field->getTypeCode());
        return $this;
    }

    /**
     * Removes the specified field.
     * Does nothing if the field does not exist.
     * 
     * @param string $fieldName name of the field.
     * 
     * @return BinaryObject the same instance of BinaryObject.
     * 
     * @throws Exception::ClientException if error.
     */
    public function removeField(string $fieldName): BinaryObject
    {
        ArgumentChecker::notEmpty($fieldName, 'fieldName');
        $this->modified = true;
        $fieldId = BinaryField::calculateId($fieldName);
        if (array_key_exists($fieldId, $this->fields)) {
            unset($this->fields[$fieldId]);
        }
        $this->typeBuilder->removeField($fieldName);
        return $this;
    }
    
    /**
     * Checks if the specified field exists in this BinaryObject instance.
     * 
     * @param string $fieldName name of the field.
     * 
     * @return bool true if exists, false otherwise.
     * 
     * @throws Exception::ClientException if error.
     */
    public function hasField(string $fieldName): bool
    {
        ArgumentChecker::notEmpty($fieldName, 'fieldName');
        $fieldId = BinaryField::calculateId($fieldName);
        return array_key_exists($fieldId, $this->fields);
    }

    /**
     * Returns a value of the specified field.
     *
     * Optionally, specifies a type of the field.
     * If the type is not specified then the Ignite client
     * will try to make automatic mapping between PHP types and Ignite object types -
     * according to the mapping table defined in the description of the ObjectType class.
     * 
     * @param string $fieldName name of the field.
     * @param int|ObjectType|null $fieldType type of the field:
     *   - either a type code of primitive (simple) type (@ref PrimitiveTypeCodes)
     *   - or an instance of class representing non-primitive (composite) type
     *   - or null (or not specified) that means the type is not specified
     * 
     * @return mixed value of the field or null if the field does not exist.
     * 
     * @throws Exception::ClientException if error.
     */
    public function getField(string $fieldName, $fieldType = null)
    {
        ArgumentChecker::notEmpty($fieldName, 'fieldName');
        BinaryUtils::checkObjectType($fieldType, 'fieldType');
        $fieldId = BinaryField::calculateId($fieldName);
        if (array_key_exists($fieldId, $this->fields)) {
            return $this->fields[$fieldId]->getValue($fieldType);
        }
        return null;
    }
    
    /**
     * Deserializes this BinaryObject instance into an instance of the specified complex object type.
     * 
     * @param ComplexObjectType $complexObjectType instance of class representing complex object type.
     * 
     * @return object instance of the PHP object which corresponds to the specified complex object type.
     * 
     * @throws Exception::ClientException if error.
     */
    public function toObject(ComplexObjectType $complexObjectType): object
    {
        $className = $complexObjectType->getPhpClassName();
        if (!$className) {
            $className = $this->getTypeName();
        }
        $result = new $className;
        foreach ($this->fields as $field) {
            $binaryField = $this->typeBuilder->getField($field->getId());
            if (!$binaryField) {
                BinaryUtils::serializationError(
                    false, sprintf('field with id "%s" can not be deserialized', $field->getId()));
            }
            $fieldName = $binaryField->getName();
            $result->$fieldName = $field->getValue($complexObjectType->getFieldType($fieldName));
        }
        return $result;
    }
    
    /**
     * Returns type name of this BinaryObject instance.
     * 
     * @return string type name.
     */
    public function getTypeName(): string
    {
        return $this->typeBuilder->getTypeName();
    }
    
    /**
     * Returns names of all fields of this BinaryObject instance.
     * 
     * @return array names of all fields.
     * 
     * @throws Exception::ClientException if error.
     */
    public function getFieldNames(): array
    {
        return array_map(
            function ($fieldId) {
                $field = $this->typeBuilder->getField($fieldId);
                if ($field) {
                    return $field->getName();
                } else {
                    BinaryUtils::internalError(
                        sprintf('Field "%s" is absent in binary type fields', $fieldId));
                }
            },
            $this->typeBuilder->getSchema()->getFieldIds());
    }

    private static function isFlagSet(int $flags, int $flag): bool
    {
        return ($flags & $flag) === $flag;
    }

    public static function fromBuffer(MessageBuffer $buffer): BinaryObject
    {
        $result = new BinaryObject(' ');
        $result->buffer = $buffer;
        $result->startPos = $buffer->getPosition();
        $result->read();
        return $result;
    }

    public function write(MessageBuffer $buffer): void
    {
        if ($this->buffer && !$this->modified) {
            $buffer->writeBuffer($this->buffer, $this->startPos, $this->length);
        } else {
            $this->typeBuilder->finalize();
            $this->startPos = $buffer->getPosition();
            $buffer->setPosition($this->startPos + BinaryObject::HEADER_LENGTH);
            // write fields
            foreach ($this->fields as $field) {
                $field->writeValue($buffer, $this->typeBuilder->getField($field->getId())->getTypeCode());
            }
            $this->schemaOffset = $buffer->getPosition() - $this->startPos;
            // write schema
            foreach ($this->fields as $field) {
                $field->writeOffset($buffer, $this->startPos);
            }
            $this->length = $buffer->getPosition() - $this->startPos;
            $this->buffer = $buffer;
            // write header
            $this->writeHeader();
            $this->buffer->setPosition($this->startPos + $this->length);
            $this->modified = false;
        }

        if (Logger::isDebug()) {
            Logger::logDebug('BinaryObject::write');
            Logger::logBuffer($this->buffer, $this->startPos, $this->length);
        }
    }

    private function writeHeader(): void
    {
        $this->buffer->setPosition($this->startPos);
        // type code
        $this->buffer->writeByte(ObjectType::COMPLEX_OBJECT);
        // version
        $this->buffer->writeByte(BinaryObject::VERSION);
        // flags
        $this->buffer->writeShort(BinaryObject::FLAG_USER_TYPE | BinaryObject::FLAG_HAS_SCHEMA | BinaryObject::FLAG_COMPACT_FOOTER);
        // type id
        $this->buffer->writeInteger($this->typeBuilder->getTypeId());
        // hash code
        $this->buffer->writeInteger(BinaryUtils::contentHashCode(
            $this->buffer, $this->startPos + BinaryObject::HEADER_LENGTH, $this->schemaOffset - 1));
        // length
        $this->buffer->writeInteger($this->length);
        // schema id
        $this->buffer->writeInteger($this->typeBuilder->getSchemaId());
        // schema offset
        $this->buffer->writeInteger($this->schemaOffset);
    }

    private function read(): void
    {
        $this->readHeader();
        $this->buffer->setPosition($this->startPos + $this->schemaOffset);
        $fieldOffsets = [];
        $fieldIds = $this->typeBuilder->getSchema()->getFieldIds();
        $index = 0;
        while ($this->buffer->getPosition() < $this->startPos + $this->length) {
            if (!$this->compactFooter) {
                $fieldId = $this->buffer->readInteger();
                $this->typeBuilder->getSchema()->addField($fieldId);
            } else {
                if ($index >= count($fieldIds)) {
                    BinaryUtils::serializationError(
                        false, 'wrong number of fields in schema');
                }
                $fieldId = $fieldIds[$index];
                $index++;
            }
            array_push($fieldOffsets, [$fieldId, $this->buffer->readNumber($this->offsetType)]);
        }
        usort($fieldOffsets, function ($val1, $val2) {
            return $val1[1] - $val2[1];
        });
        for ($i = 0; $i < count($fieldOffsets); $i++) {
            $fieldId = $fieldOffsets[$i][0];
            $offset = $fieldOffsets[$i][1];
            $nextOffset = $i + 1 < count($fieldOffsets) ? $fieldOffsets[$i + 1][1] : $this->schemaOffset;
            $field = BinaryObjectField::fromBuffer(
                $this->buffer, $this->startPos + $offset, $nextOffset - $offset, $fieldId);
            $this->fields[$field->getId()] = $field;
        }
        $this->buffer->setPosition($this->startPos + $this->length);
    }

    private function readHeader(): void
    {
        // type code
        $this->buffer->readByte();
        // version
        $version = $this->buffer->readByte();
        if ($version !== BinaryObject::VERSION) {
            BinaryUtils::internalError();
        }
        // flags
        $flags = $this->buffer->readShort();
        // type id
        $typeId = $this->buffer->readInteger();
        // hash code
        $this->buffer->readInteger();
        // length
        $this->length = $this->buffer->readInteger();
        // schema id
        $schemaId = $this->buffer->readInteger();
        // schema offset
        $this->schemaOffset = $this->buffer->readInteger();
        $hasSchema = BinaryObject::isFlagSet($flags, BinaryObject::FLAG_HAS_SCHEMA);
        $this->compactFooter = BinaryObject::isFlagSet($flags, BinaryObject::FLAG_COMPACT_FOOTER);
        $this->offsetType = BinaryObject::isFlagSet($flags, BinaryObject::FLAG_OFFSET_ONE_BYTE) ?
            ObjectType::BYTE :
            BinaryObject::isFlagSet($flags, BinaryObject::FLAG_OFFSET_TWO_BYTES) ?
                ObjectType::SHORT :
                ObjectType::INTEGER;

        if (BinaryObject::isFlagSet($flags, BinaryObject::FLAG_HAS_RAW_DATA)) {
            BinaryUtils::serializationError(
                false, 'complex objects with raw data are not supported');
        }
        if ($this->compactFooter && !$hasSchema) {
            BinaryUtils::serializationError(
                false, 'schema is absent for object with compact footer');
        }
        $this->typeBuilder = BinaryTypeBuilder::fromTypeId($typeId, $schemaId, $hasSchema);
    }
}
