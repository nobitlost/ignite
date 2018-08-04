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

namespace Apache\Ignite\Impl\Binary;

use Ds\Map;
use Ds\Set;
use Brick\Math\BigDecimal;
use Apache\Ignite\Exception\ClientException;
use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Type\MapObjectType;
use Apache\Ignite\Type\CollectionObjectType;
use Apache\Ignite\Type\ComplexObjectType;
use Apache\Ignite\Data\Date;
use Apache\Ignite\Data\Time;
use Apache\Ignite\Data\Timestamp;
use Apache\Ignite\Data\BinaryObject;
use Apache\Ignite\Impl\Utils\ArgumentChecker;

class BinaryUtils
{
    const FLOAT_EPSILON = 0.00001;
    
    public static function getSize(int $typeCode): int
    {
        return TypeInfo::getTypeInfo($typeCode)->getSize();
    }
    
    public static function checkCompatibility($value, $type): void
    {
        // TODO
    }
    
    public static function checkTypesComatibility($expectedType, int $actualTypeCode): void
    {
        // TODO
    }

    public static function calcObjectType($object)
    {
        if ($object === null) {
            return ObjectType::NULL;
        } elseif (is_integer($object)) {
            return ObjectType::INTEGER;
        } elseif (is_float($object)) {
            return ObjectType::DOUBLE;
        } elseif (is_string($object)) {
            return ObjectType::STRING;
        } elseif (is_bool($object)) {
            return ObjectType::BOOLEAN;
        } elseif (is_array($object)) {
            if (count($object) > 0) {
                $values = array_values($object);
                $firstElem = $values[0];
                if ($firstElem !== null) {
                    if ($values === $object) {
                        // sequential array
                        return BinaryUtils::getArrayType(BinaryUtils::calcObjectType($firstElem));
                    } else {
                        // associative array
                        return new MapObjectType();
                    }
                }
            }
        } elseif ($object instanceof Time) {
            return ObjectType::TIME;
        } elseif ($object instanceof Timestamp) {
            return ObjectType::TIMESTAMP;
        } elseif ($object instanceof Date) {
            return ObjectType::DATE;
        } elseif ($object instanceof EnumItem) {
            return ObjectType::ENUM;
        } elseif ($object instanceof BigDecimal) {
            return ObjectType::DECIMAL;
        } elseif ($object instanceof Set) {
            return new CollectionObjectType(CollectionObjectType::HASH_SET);
        } elseif ($object instanceof Map) {
            return new MapObjectType();
        } elseif ($object instanceof BinaryObject) {
            return ObjectType::BINARY_OBJECT;
        } elseif (is_object($object)) {
            return new ComplexObjectType();
        }
        BinaryUtils::unsupportedType(gettype($object));
    }
    
    public static function getArrayType($elementType)
    {
        switch (BinaryUtils::getTypeCode($elementType)) {
            case ObjectType::BYTE:
                return ObjectType::BYTE_ARRAY;
            case ObjectType::SHORT:
                return ObjectType::SHORT_ARRAY;
            case ObjectType::INTEGER:
                return ObjectType::INTEGER_ARRAY;
            case ObjectType::LONG:
                return ObjectType::LONG_ARRAY;
            case ObjectType::FLOAT:
                return ObjectType::FLOAT_ARRAY;
            case ObjectType::DOUBLE:
                return ObjectType::DOUBLE_ARRAY;
            case ObjectType::CHAR:
                return ObjectType::CHAR_ARRAY;
            case ObjectType::BOOLEAN:
                return ObjectType::BOOLEAN_ARRAY;
            case ObjectType::STRING:
                return ObjectType::STRING_ARRAY;
            case ObjectType::UUID:
                return ObjectType::UUID_ARRAY;
            case ObjectType::DATE:
                return ObjectType::DATE_ARRAY;
            case ObjectType::ENUM:
                return ObjectType::ENUM_ARRAY;
            case ObjectType::DECIMAL:
                return ObjectType::DECIMAL_ARRAY;
            case ObjectType::TIMESTAMP:
                return ObjectType::TIMESTAMP_ARRAY;
            case ObjectType::TIME:
                return ObjectType::TIME_ARRAY;
            default:
                BinaryUtils::unsupportedType(BinaryUtils::getTypeName($elementType));
        }
    }
    
    public static function getArrayElementType($arrayType)
    {
//        if ($arrayType instanceof ObjectArrayType) {
//            return $arrayType->elementType;
//        } elseif ($arrayType === ObjectType::OBJECT_ARRAY) {
//            return null;
//        }
        $info = TypeInfo::getTypeInfo($arrayType);
        if (!$info || !$info->getElementTypeCode()) {
            BinaryUtils::internalError();
        }
        return $info->getElementTypeCode();
    }
    
    public static function getTypeCode($objectType): int
    {
        return $objectType instanceof ObjectType ? $objectType->getTypeCode() : $objectType;
    }
    
    public static function getTypeName($objectType): string
    {
        if (is_string($objectType)) {
            return $objectType;
        }
        $typeCode = BinaryUtils::getTypeCode($objectType);
        $info = TypeInfo::getTypeInfo($typeCode);
        return $info ? $info->getName() : 'type code ' . $typeCode;
    }
    
    public static function checkObjectType($type, string $argName): void
    {
        if ($type === null || $type instanceof ObjectType) {
            return;
        }
        ArgumentChecker::hasValueFrom($type, $argName, false, TypeInfo::getPrimitiveTypes());
    }
    
    public static function floatEquals(float $val1, float $val2): bool
    {
        return abs($val1 - $val2) < BinaryUtils::FLOAT_EPSILON;
    }
    
    public static function hashCode(?string $str): int
    {
        $hash = 0;
        $length = strlen($str);
        if ($str && $length > 0) {
            for ($i = 0; $i < $length; $i++) {
                $hash = (($hash << 5) - $hash) + ord($str[$i]);
                $hash &= 0xFFFFFFFF; // Convert to 32bit integer
            }
        }
        return BinaryUtils::intval32($hash);
    }
    
    public static function hashCodeLowerCase(?string $str): int
    {
        return BinaryUtils::hashCode($str ? strtolower($str) : $str);
    }

    public static function contentHashCode(MessageBuffer $buffer, int $startPos, int $endPos): int
    {
        $hash = 1;
        $length = $endPos - $startPos + 1;
        $content = $buffer->getSlice($startPos, $length);
        for ($i = 0; $i < $length; $i++) {
            $hash = 31 * $hash + ord($content[$i]);
            $hash &= 0xFFFFFFFF; // Convert to 32bit integer
        }
        return BinaryUtils::intval32($hash);
    }
    
    public static function intval32(int $value): int
    {
        $value = ($value & 0xFFFFFFFF);
        if ($value & 0x80000000) {
            $value = -((~$value & 0xFFFFFFFF) + 1);
        }
        return $value;
    }
    
    public static function internalError(string $message = null): void
    {
        throw new ClientException($message || 'Internal library error');
    }
    
    public static function unsupportedType($type): void
    {
        throw new ClientException(sprintf('Type %s is not supported', BinaryUtils::getTypeName($type)));
    }
    
    public static function serializationError(bool $serialize, string $message = null): void
    {
        $msg = $serialize ? 'Complex object can not be serialized' : 'Complex object can not be deserialized';
        if ($message) {
            $msg = $msg . ': ' . $message;
        }
        throw new ClientException($msg);
    }
}
