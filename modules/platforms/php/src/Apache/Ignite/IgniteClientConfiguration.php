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

namespace Apache\Ignite;

class IgniteClientConfiguration {
    private $endpoints;
    private $userName;
    private $password;
    
    public function __construct(...$endpoints) {
        $this->endpoints = $endpoints;
        $this->userName = null;
        $this->password = null;
    }
    
    public function getEndpoints(): array {
        return $this->endpoints;
    }
    
    public function getUserName(): ?string {
        return $this->userName;
    }
    
    public function setUserName(string $userName): IgniteClientConfiguration {
        $this->userName = $userName;
        return $this;
    }
    
    public function getPassword(): ?string {
        return $this->password;
    }
    
    public function setPassword(string $password): IgniteClientConfiguration {
        $this->password = $password;
        return $this;
    }
}

?>
