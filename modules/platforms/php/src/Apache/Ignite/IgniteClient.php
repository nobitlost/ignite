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

use Apache\Ignite\Impl\Connection\ClientFailoverSocket as ClientFailoverSocket;
use Apache\Ignite\Impl\Binary\MessageBuffer as MessageBuffer;
use Apache\Ignite\Impl\Utils\ArgumentChecker as ArgumentChecker;
use Apache\Ignite\Impl\Utils\Logger as Logger;
use Apache\Ignite\Impl\Binary\ClientOperation as ClientOperation;
use Apache\Ignite\Impl\Binary\BinaryWriter as BinaryWriter;
use Apache\Ignite\Impl\CacheClient as CacheClient;

class IgniteClient {
    const STATE_DISCONNECTED = 0;
    const STATE_CONNECTING = 1;
    const STATE_CONNECTED = 2;
    
    private $socket;
    
    public function __construct(callable $onStateChanged = null) {
        $this->socket = new ClientFailoverSocket($onStateChanged);
    }
    
    public function connect(IgniteClientConfiguration $config): void {
        $this->socket->connect($config);
    }
    
    public function disconnect(): void {
        if ($this->socket) {
            $this->socket->disconnect();
        }
    }
    
    public function createCache(
            string $name,
            CacheConfiguration $cacheConfig = null): CacheClientInterface {
        ArgumentChecker::notEmpty($name, 'name');
        $this->socket->send(
            $cacheConfig ?
                ClientOperation::CACHE_CREATE_WITH_CONFIGURATION :
                ClientOperation::CACHE_CREATE_WITH_NAME,
            function (MessageBuffer $payload) use ($name, $cacheConfig) {
                $this->writeCacheNameOrConfig($payload, $name, $cacheConfig);
            });
        return $this->getCacheClient($name, $cacheConfig);
    }
    
    public function getOrCreateCache(
            string $name,
            CacheConfiguration $cacheConfig = null): CacheClientInterface {
        ArgumentChecker::notEmpty($name, 'name');
        $this->socket->send(
            $cacheConfig ?
                ClientOperation::CACHE_GET_OR_CREATE_WITH_CONFIGURATION :
                ClientOperation::CACHE_GET_OR_CREATE_WITH_NAME,
            function (MessageBuffer $payload) use ($name, $cacheConfig) {
                $this->writeCacheNameOrConfig($payload, $name, $cacheConfig);
            });
        return $this->getCacheClient($name, $cacheConfig);
    }
    
    public function getCache(string $name): CacheClientInterface {
        ArgumentChecker::notEmpty($name, 'name');
        return $this->getCacheClient($name);
    }
    
    public function destroyCache(string $name): void {
        ArgumentChecker::notEmpty($name, 'name');
        $this->socket->send(
            ClientOperation::CACHE_DESTROY,
            function (MessageBuffer $payload) use ($name) {
                $payload->writeInteger(CacheClient::calculateId($name));
            });
    }
    
    public function setDebug(bool $value): void {
        Logger::setDebug($value);
    }
    
    private function getCacheClient(
            string $name,
            CacheConfiguration $cacheConfig = null): CacheClientInterface {
        return new CacheClient($name, $cacheConfig, $this->socket);
    }
    
    private function writeCacheNameOrConfig(
            MessageBuffer $buffer,
            string $name,
            CacheConfiguration $cacheConfig = null): void {
        if ($cacheConfig) {
            $cacheConfig->write($buffer, $name);
        }
        else {
            BinaryWriter::writeString($buffer, $name);
        }
    }
}

?>
