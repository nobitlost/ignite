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

class BinaryUtils {
    public static function getSize(int $typeCode): int {
        return TypeInfo::getTypeInfo($typeCode)->getSize();
    }
    
    public static function checkCompatibility($value, $type): void {
        // TODO
    }
    
    public static function checkTypesComatibility($expectedType, $actualTypeCode): void {
        // TODO
    }

    public static function calcObjectType($object) {
        if ($object === null) {
            return TypeInfo::TYPE_NULL;
        }
        else if (is_integer($object)) {
            return TypeInfo::TYPE_INTEGER;
        }
        else if (is_float($object)) {
            return TypeInfo::TYPE_DOUBLE;
        }        
        else if (is_string($object)) {
            return TypeInfo::TYPE_STRING;
        }
        else if (is_bool($object)) {
            return TypeInfo::TYPE_BOOLEAN;
        }
        throw IgniteClientException::unsupportedTypeException(gettype($object));
    }
    
    public static function getTypeCode($objectType): int {
        // TODO
        return $objectType;        
    }
    
    public static function hashCode($str) {
        $hash = 0;
        $length = strlen($str);
        if ($str && $length > 0) {
            for ($i = 0; $i < $length; $i++) {
                $hash = (($hash << 5) - $hash) + ord($str[$i]);
            }
        }
        return $hash;
    }
}

?>
