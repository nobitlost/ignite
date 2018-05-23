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

use Apache\Ignite\Exception\IgniteClientException as IgniteClientException;

class BinaryWriter {
    public static function writeString(MessageBuffer $buffer, ?string $value): void {
        BinaryWriter::writeObject($buffer, $value, TypeInfo::TYPE_STRING);
    }

    public static function writeObject(MessageBuffer $buffer, $object, $objectType = null, bool $writeObjectType = true): void {
        BinaryUtils::checkCompatibility($object, $objectType);
        if ($object === null) {
            $buffer->writeByte(TypeInfo::TYPE_NULL);
            return;
        }

        $objectType = $objectType ? $objectType : BinaryUtils::calcObjectType($object);
        $objectTypeCode = BinaryUtils::getTypeCode($objectType);

        if ($writeObjectType) {
            $buffer->writeByte($objectTypeCode);
        }
        switch ($objectTypeCode) {
            case TypeInfo::TYPE_BYTE:
            case TypeInfo::TYPE_SHORT:
            case TypeInfo::TYPE_INTEGER:
            case TypeInfo::TYPE_LONG:
            case TypeInfo::TYPE_FLOAT:
            case TypeInfo::TYPE_DOUBLE:
                $buffer->writeNumber($object, $objectTypeCode);
                break;
            case TypeInfo::TYPE_BOOLEAN:
                $buffer->writeBoolean($object);
                break;
            case TypeInfo::TYPE_STRING:
                $buffer->writeString($object);
                break;
            default:
                throw IgniteClientException::unsupportedTypeException($objectType);
        }
    }
}

?>
