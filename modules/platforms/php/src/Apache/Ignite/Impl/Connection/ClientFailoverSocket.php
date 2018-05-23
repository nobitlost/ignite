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

namespace Apache\Ignite\Impl\Connection;

use Apache\Ignite\IgniteClient as IgniteClient;
use Apache\Ignite\IgniteClientConfiguration as IgniteClientConfiguration;
use Apache\Ignite\Exception\IllegalStateException as IllegalStateException;
use Apache\Ignite\Impl\Utils\Logger as Logger;

class ClientFailoverSocket {
    private $socket;
    private $state;
    private $onStateChanged;
            
    public function __construct(callable $onStateChanged = null) {
        $this->socket = null;
        $this->state = IgniteClient::STATE_DISCONNECTED;
        $this->onStateChanged = $onStateChanged;
    }

    public function connect(IgniteClientConfiguration $config): void {
        if ($this->state !== IgniteClient::STATE_DISCONNECTED) {
            throw new IllegalStateException();
        }
        $this->config = $config;
        $this->socket = new ClientSocket(
                $this->config->getEndpoints()[0],
                $this->config,
                array($this, 'onSocketDisconnect'));
        $this->changeState(IgniteClient::STATE_CONNECTING);
        $this->socket->connect();
        $this->changeState(IgniteClient::STATE_CONNECTED);
    }

    public function send(int $opCode, callable $payloadWriter, callable $payloadReader = null): void {
        if ($this->state !== IgniteClient::STATE_CONNECTED) {
            throw new IllegalStateException();
        }
        $this->socket->sendRequest($opCode, $payloadWriter, $payloadReader);
    }

    public function disconnect(): void {
        if ($this->state !== IgniteClient::STATE_DISCONNECTED) {
            $this->changeState(IgniteClient::STATE_DISCONNECTED);
            if ($this->socket) {
                $this->socket->disconnect();
                $this->socket = null;
            }
        }
    }

    public function onSocketDisconnect(string $error = null): void {
        $this->changeState(IgniteClient::STATE_DISCONNECTED, $error);
        $this->socket = null;
    }

    private function changeState(int $state, string $reason = null): void {
        if (Logger::isDebug() && $this->socket) {
            Logger::logDebug(sprintf('Socket %s: %s -> %s',
                $this->socket->getEndpoint(), $this->getState($this->state), $this->getState($state)));
        }
        $this->state = $state;
        if ($this->onStateChanged) {
            call_user_func($this->onStateChanged($state, $reason));
        }
    }

    private function getState(int $state) {
        switch ($state) {
            case IgniteClient::STATE_DISCONNECTED:
                return 'DISCONNECTED';
            case IgniteClient::STATE_CONNECTING:
                return 'CONNECTING';
            case IgniteClient::STATE_CONNECTED:
                return 'CONNECTED';
            default:
                return 'UNKNOWN';
        }
    }
}

?>
