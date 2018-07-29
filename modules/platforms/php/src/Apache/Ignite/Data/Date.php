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
 * Class representing an Ignite Date type.
 */
class Date
{
    private $millis;

    /**
     * Public constructor.
     * 
     * @param float $millis integer value representing number of milliseconds since January 1, 1970, 00:00:00 UTC.
     */
    public function __construct(float $millis)
    {
        $this->millis = $millis;
    }
    
    /**
     * Returns number of milliseconds since January 1, 1970, 00:00:00 UTC.
     * 
     * @return float number of milliseconds since January 1, 1970, 00:00:00 UTC.
     */
    public function getMillis(): float
    {
        return $this->millis;
    }
    
    /**
     * Returns number of seconds since January 1, 1970, 00:00:00 UTC.
     * 
     * @return float number of seconds since January 1, 1970, 00:00:00 UTC.
     */
    public function getSeconds(): float
    {
        return $this->millis / 1000;
    }
    
    /**
     * Creates an Date object from a DateTime object.
     * 
     * @param DateTime $dateTime a DateTime object.
     * 
     * @return Date created Date object.
     */
    public static function fromDateTime(DateTime $dateTime)
    {
        return new Date($dateTime->getTimestamp() * 1000);
    }
    
    /**
     * Returns a DateTime object representing this Date.
     * 
     * @return DateTime
     */
    public function toDateTime(): DateTime
    {
        $dateTime = new DateTime();
        $dateTime->setTimestamp($this->getSeconds());
        return $dateTime;
    }
}
