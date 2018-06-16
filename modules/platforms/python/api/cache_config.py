# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Set of functions to manipulate caches.

Ignite `cache` can be viewed as a named entity designed to store key-value
pairs. Each cache is split transparently between different Ignite partitions.

The choice of `cache` term is due to historical reasons. (Ignite initially had
only non-persistent storage tier.)
"""

from connection import Connection
from datatypes.cache_config import cache_config_struct
from datatypes.primitive import Int, Byte
from datatypes.strings import String, StringArray
from queries.op_codes import *
from queries import Query, Response
from .result import APIResult


class CacheGetConfigurationQuery(Query):
    op_code = OP_CACHE_GET_CONFIGURATION


class CacheGetNamesQuery(Query):
    op_code = OP_CACHE_GET_NAMES


class CacheCreateQuery(Query):
    op_code = OP_CACHE_CREATE_WITH_NAME


class CacheGetOrCreateQuery(Query):
    op_code = OP_CACHE_GET_OR_CREATE_WITH_NAME


class CacheDestroyQuery(Query):
    op_code = OP_CACHE_DESTROY


def cache_get_configuration(
    conn: Connection, hash_code: int, flags: int=0
) -> APIResult:
    """
    Gets configuration for the given cache.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param flags: Ignite documentation is unclear on this subject,
    :return: API result data object. Result value is OrderedDict with
     the cache configuration parameters.
    """

    query_struct = CacheGetConfigurationQuery([
        ('hash_code', Int),
        ('flags', Byte),
    ])

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flags': flags,
    })
    conn.send(send_buffer)

    response_struct = Response([
        ('cache_config', cache_config_struct),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)
    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['cache_config']
    return result


def cache_create(conn: Connection, name: str) -> APIResult:
    """
    Creates a cache with a given name. Returns error if a cache with specified
    name already exists.

    :param conn: connection to Ignite server,
    :param name: cache name,
    :return: API result data object. Contains zero status if a cache is
     created successfully, non-zero status and an error description otherwise.
    """

    query_struct = CacheCreateQuery([
        ('cache_name', String),
    ])
    _, send_buffer = query_struct.from_python({'cache_name': name})
    conn.send(send_buffer)

    response_struct = Response([])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)
    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    return result


def cache_get_or_create(conn: Connection, name: str) -> APIResult:
    """
    Creates a cache with a given name. Does nothing if the cache exists.

    :param conn: connection to Ignite server,
    :param name: cache name,
    :return: API result data object. Contains zero status if a cache is
     created successfully, non-zero status and an error description otherwise.
    """

    query_struct = CacheGetOrCreateQuery([
        ('cache_name', String),
    ])
    _, send_buffer = query_struct.from_python({'cache_name': name})
    conn.send(send_buffer)

    response_struct = Response([])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)
    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    return result


def cache_destroy(conn: Connection, hash_code: int) -> APIResult:
    """
    Destroys cache with a given name.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :return: API result data object.
    """

    query_struct = CacheDestroyQuery([
        ('hash_code', Int),
    ])

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
    })
    conn.send(send_buffer)

    response_struct = Response([])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)
    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    return result


def cache_get_names(conn: Connection) -> APIResult:
    """
    Gets existing cache names.

    :param conn: connection to Ignite server,
    :return: API result data object. Contains zero status and a list of cache
     names, non-zero status and an error description otherwise.
    """

    query_struct = CacheGetNamesQuery()

    _, send_buffer = query_struct.from_python()
    conn.send(send_buffer)

    response_struct = Response([
        ('cache_names', StringArray),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)
    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['cache_names']
    return result
