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

namespace Apache\Ignite\Tests;

use Apache\Ignite\IgniteClient;
use Apache\Ignite\IgniteClientConfiguration;
use Apache\Ignite\Exception\OperationException;

/**
 * Helper class for testing apache-ignite-client library.
 * Contains common methods for testing environment initialization and cleanup.
 */
class TestingHelper
{
    private static $igniteClient;
    
    /**
     * Initializes testing environment: creates and starts the library client, sets default jasmine test timeout.
     * Should be called from any test case setUpBeforeClass method.
     */
    public static function init(): void
    {
        TestingHelper::$igniteClient = new IgniteClient();
        TestingHelper::$igniteClient->connect(new IgniteClientConfiguration(...TestConfig::$endpoints));
        TestingHelper::$igniteClient->setDebug(TestConfig::$debug);
    }

    /**
     * Cleans up testing environment.
     * Should be called from any test case tearDownAfterClass method.
     */
    public static function cleanUp(): void
    {
        TestingHelper::$igniteClient->disconnect();
    }

    public static function getIgniteClient(): IgniteClient
    {
        return TestingHelper::$igniteClient;
    }
    
    public static function destroyCache(string $cacheName) : void
    {
        try {
            TestingHelper::$igniteClient->destroyCache($cacheName);
        }
        catch (OperationException $e) {
            //expected exception
        }
    }
}