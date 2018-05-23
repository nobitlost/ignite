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

class BinaryReader {
    public static function readObject(MessageBuffer $buffer, $expectedType = null) {
        $typeCode = $buffer->readByte();
        BinaryUtils::checkTypesComatibility($expectedType, $typeCode);
        return BinaryReader::readTypedObject($buffer, $typeCode, $expectedType);
    }
    
    private static function readTypedObject(MessageBuffer $buffer, int $objectTypeCode, $expectedType = null) {
        switch ($objectTypeCode) {
            case TypeInfo::TYPE_BYTE:
            case TypeInfo::TYPE_SHORT:
            case TypeInfo::TYPE_INTEGER:
            case TypeInfo::TYPE_LONG:
            case TypeInfo::TYPE_FLOAT:
            case TypeInfo::TYPE_DOUBLE:
                return $buffer->readNumber($objectTypeCode);
            case TypeInfo::TYPE_BOOLEAN:
                return $buffer->readBoolean();
            case TypeInfo::TYPE_STRING:
                return $buffer->readString();
            default:
                throw IgniteClientException::unsupportedTypeException($objectTypeCode);
        }
    }
}

?>
