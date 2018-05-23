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

namespace Apache\Ignite\Exception;

use Apache\Ignite\Impl\Binary\BinaryUtils as BinaryUtils;

/**
 * Base Ignite client exception class.
 */
class IgniteClientException extends \Exception {
    public function __construct(string $message) {
        parent::__construct($message);
    }

    /**
     * Ignite client does not support one of the specified or received data types.
     */
    public static function unsupportedTypeException($type): IgniteClientException {
        return new IgniteClientException(sprintf('Type %s is not supported', BinaryUtils::getTypeName($type)));
    }

    /**
     * An illegal or inappropriate argument has been passed to the API method.
     */
    public static function illegalArgumentException(?string $message) {
        return new IgniteClientException($message);
    }

    /**
     * Ignite client internal error.
     */
    public static function internalError(?string $message = null) {
        return new IgniteClientException($message || 'Internal library error');
    }
}

?>
