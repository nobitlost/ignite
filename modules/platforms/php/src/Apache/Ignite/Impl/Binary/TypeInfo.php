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

use Apache\Ignite\ObjectType\PrimitiveObjectType as PrimitiveObjectType;

class TypeInfo {
    const TYPE_BYTE = PrimitiveObjectType::BYTE;
    const TYPE_SHORT = PrimitiveObjectType::SHORT;
    const TYPE_INTEGER = PrimitiveObjectType::INTEGER;
    const TYPE_LONG = PrimitiveObjectType::LONG;
    const TYPE_FLOAT = PrimitiveObjectType::FLOAT;
    const TYPE_DOUBLE = PrimitiveObjectType::DOUBLE;
    const TYPE_BOOLEAN = PrimitiveObjectType::BOOLEAN;
    const TYPE_STRING = PrimitiveObjectType::STRING;
    const TYPE_NULL = 101;

    private $name;
    private $size;
    private $nullable;
    
    private static $info;
    
    static function init(): void {
        TypeInfo::$info = array(
            TypeInfo::TYPE_BYTE => new TypeInfo('byte', 1),
            TypeInfo::TYPE_SHORT => new TypeInfo('short', 2),
            TypeInfo::TYPE_INTEGER => new TypeInfo('integer', 4),
            TypeInfo::TYPE_LONG => new TypeInfo('long', 8),
            TypeInfo::TYPE_FLOAT => new TypeInfo('float', 4),
            TypeInfo::TYPE_DOUBLE => new TypeInfo('double', 8),
            TypeInfo::TYPE_BOOLEAN => new TypeInfo('boolean', 1),
            TypeInfo::TYPE_STRING => new TypeInfo('string', 0, true)
        );
    }
    
    static function getTypeInfo(int $typeCode): TypeInfo {
        return TypeInfo::$info[$typeCode];
    }
    
    private function __construct(string $name, int $size, bool $nullable = false) {
        $this->name = $name;
        $this->size = $size;
        $this->nullable = $nullable;
    }
    
    public function getName(): string {
        return $this->name;
    }

    public function getSize(): int {
        return $this->size;
    }
    
    public function isNullable(): bool {
        return $this->nullable;
    }
}

TypeInfo::init();

?>
