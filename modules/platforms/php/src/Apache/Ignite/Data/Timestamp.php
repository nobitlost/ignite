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

namespace Apache\Ignite\Data;

use \DateTime;

/** 
 * Class representing an Ignite Timestamp type.
 */
class Timestamp extends Date
{
    private $nanos;

    /**
     * Public constructor.
     * 
     * @param float $millis integer value representing number of milliseconds since 
     *                         January 1, 1970, 00:00:00 UTC.
     * @param int $nanos nanoseconds of the last millisecond, should be in the range from 0 to 999999.
     */
    public function __construct(float $millis, int $nanos)
    {
        parent::__construct($millis);
        $this->nanos = $nanos;
    }
    
    /**
     * Returns the nanoseconds of the last millisecond from the timestamp.
     * 
     * @return float nanoseconds of the last millisecond.
     */
    public function getNanos(): int
    {
        return $this->nanos;
    }
    
    /**
     * Creates an Timestamp object from a DateTime object.
     * 
     * @param DateTime $dateTime a DateTime object.
     * 
     * @return Timestamp created Timestamp object.
     */
    public static function fromDateTime(DateTime $dateTime)
    {
        return new Timestamp($dateTime->getTimestamp() * 1000, 0);
    }
}
