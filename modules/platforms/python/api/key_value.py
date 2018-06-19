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

from connection import Connection
from queries.op_codes import *
from .result import APIResult

from datatypes.cache_config import StructArray
from datatypes.complex import AnyDataObject
from datatypes.primitive import Bool, Byte, Int
from queries import Query, Response
from utils import is_hinted


def cache_put(
    conn: Connection, hash_code: int, key, value,
    key_hint=None, value_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Puts a value with a given key to cache (overwriting existing value if any).

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param value: value for the key,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param value_hint: (optional) Ignite data type, for which the given value
     should be converted.
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status if a value
     is written, non-zero status and an error description otherwise.
    """

    class CachePutQuery(Query):
        op_code = OP_CACHE_PUT

    query_struct = CachePutQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
        ('value', value_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
        'value': value,
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
    result.value = response_struct.to_python(response)
    return result


def cache_get(
    conn: Connection, hash_code: int, key,
    key_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Retrieves a value from cache by key.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and a value
     retrieved on success, non-zero status and an error description on failure.
    """

    class CacheGetQuery(Query):
        op_code = OP_CACHE_GET

    query_struct = CacheGetQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('value', AnyDataObject),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['value']
    return result


def cache_get_all(
    conn: Connection, hash_code: int, keys: list, binary=False, query_id=None,
) -> APIResult:
    """
    Retrieves multiple key-value pairs from cache.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param keys: list of keys or tuples of (key, key_hint),
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and a dict, made of
     retrieved key-value pairs, non-zero status and an error description
     on failure.
    """

    class CacheGetAllQuery(Query):
        op_code = OP_CACHE_GET_ALL

    value_hint_pairs = []
    length = len(keys)
    for key_or_pair in keys:
        if is_hinted(key_or_pair):
            value_hint_pairs.append(key_or_pair)
        else:
            value_hint_pairs.append((key_or_pair, AnyDataObject))

    # structure name: hint
    key_fields = {}
    # structure name: value
    data = {}
    for i, pair in enumerate(value_hint_pairs):
        name = 'element_{}'.format(i)
        value, hint = pair
        key_fields[name] = hint
        data[name] = value

    query_struct = CacheGetAllQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('length', Int),
    ] + list(key_fields.items()), query_id=query_id)

    data.update({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'length': length,
    })
    _, send_buffer = query_struct.from_python(data)
    conn.send(send_buffer)

    response_struct = Response([
        (
            'data', StructArray([
                ('key', AnyDataObject),
                ('value', AnyDataObject),
            ])
        ),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message

    result.value = {}
    for i in range(response.data.length):
        key = AnyDataObject.to_python(
            getattr(response.data, 'element_{}'.format(i)).key
        )
        value = AnyDataObject.to_python(
            getattr(response.data, 'element_{}'.format(i)).value
        )
        result.value[key] = value
    return result


def cache_put_all(
    conn: Connection, hash_code: int, pairs: dict, binary=False, query_id=None,
) -> APIResult:
    """
    Puts multiple key-value pairs to cache (overwriting existing associations
    if any).

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param pairs: dictionary type parameters, contains key-value pairs to save.
     Each key or value can be an item of representable Python type or a tuple
     of (item, hint),
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status if key-value pairs
     are written, non-zero status and an error description otherwise.
    """

    class CachePutAllQuery(Query):
        op_code = OP_CACHE_PUT_ALL

    length = len(pairs)
    unrolled = []
    for k_pair, v_pair in pairs.items():
        if not is_hinted(k_pair):
            k_pair = (k_pair, AnyDataObject)
        unrolled.append(k_pair)
        if not is_hinted(v_pair):
            v_pair = (v_pair, AnyDataObject)
        unrolled.append(v_pair)

    # structure name: hint
    key_fields = {}
    # structure name: value:
    data = {}
    for i, pair in enumerate(unrolled):
        name = 'element_{}'.format(i)
        value, hint = pair
        key_fields[name] = hint
        data[name] = value

    query_struct = CachePutAllQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('length', Int),
    ] + list(key_fields.items()), query_id=query_id)

    data.update({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'length': length,
    })
    _, send_buffer = query_struct.from_python(data)
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


def cache_contains_key(
    conn: Connection, hash_code: int, key,
    key_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Returns a value indicating whether given key is present in cache.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and a bool value
     retrieved on success: `True` when key is present, `False` otherwise,
     non-zero status and an error description on failure.
    """

    class CacheContainsKeyQuery(Query):
        op_code = OP_CACHE_CONTAINS_KEY

    query_struct = CacheContainsKeyQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('value', Bool),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['value']
    return result


def cache_contains_keys(
    conn: Connection, hash_code: int, keys, binary=False, query_id=None,
) -> APIResult:
    """
    Returns a value indicating whether all given keys are present in cache.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param keys:
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and a bool value
     retrieved on success: `True` when all keys are present, `False` otherwise,
     non-zero status and an error description on failure.
    """

    class CacheContainsKeysQuery(Query):
        op_code = OP_CACHE_CONTAINS_KEYS

    value_hint_pairs = []
    length = len(keys)
    for key_or_pair in keys:
        if is_hinted(key_or_pair):
            value_hint_pairs.append(key_or_pair)
        else:
            value_hint_pairs.append((key_or_pair, AnyDataObject))

    # structure name: hint
    key_fields = {}
    # structure name: value
    data = {}
    for i, pair in enumerate(value_hint_pairs):
        name = 'element_{}'.format(i)
        value, hint = pair
        key_fields[name] = hint
        data[name] = value

    query_struct = CacheContainsKeysQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('length', Int),
    ] + list(key_fields.items()), query_id=query_id)

    data.update({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'length': length,
    })

    _, send_buffer = query_struct.from_python(data)
    conn.send(send_buffer)

    response_struct = Response([
        ('value', Bool),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['value']
    return result


def cache_get_and_put(
    conn: Connection, hash_code: int, key, value,
    key_hint=None, value_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Puts a value with a given key to cache, and returns the previous value
    for that key, or null value if there was not such key.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param value: value for the key,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param value_hint: (optional) Ignite data type, for which the given value
     should be converted.
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and an old value
    or None if a value is written, non-zero status and an error description
    in case of error.
    """

    class CacheGetAndPutQuery(Query):
        op_code = OP_CACHE_GET_AND_PUT

    query_struct = CacheGetAndPutQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
        ('value', value_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
        'value': value,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('value', AnyDataObject),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['value']
    return result


def cache_get_and_replace(
    conn: Connection, hash_code: int, key, value,
    key_hint=None, value_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Puts a value with a given key to cache, returning previous value
    for that key, if and only if there is a value currently mapped
    for that key.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param value: value for the key,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param value_hint: (optional) Ignite data type, for which the given value
     should be converted.
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and an old value
    or None on success, non-zero status and an error description otherwise.
    """

    class CacheGetAndReplaceQuery(Query):
        op_code = OP_CACHE_GET_AND_REPLACE

    query_struct = CacheGetAndReplaceQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
        ('value', value_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
        'value': value,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('value', AnyDataObject),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['value']
    return result


def cache_get_and_remove(
    conn: Connection, hash_code: int, key,
    key_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Removes the cache entry with specified key, returning the value.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and an old value
    or None, non-zero status and an error description otherwise.
    """

    class CacheGetAndRemoveQuery(Query):
        op_code = OP_CACHE_GET_AND_REMOVE

    query_struct = CacheGetAndRemoveQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('value', AnyDataObject),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['value']
    return result


def cache_put_if_absent(
    conn: Connection, hash_code: int, key, value,
    key_hint=None, value_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Puts a value with a given key to cache only if the key
    does not already exist.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param value: value for the key,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param value_hint: (optional) Ignite data type, for which the given value
     should be converted.
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status on success,
     non-zero status and an error description otherwise.
    """

    class CachePutIfAbsentQuery(Query):
        op_code = OP_CACHE_PUT_IF_ABSENT

    query_struct = CachePutIfAbsentQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
        ('value', value_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
        'value': value,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('success', Bool),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['success']
    return result


def cache_get_and_put_if_absent(
    conn: Connection, hash_code: int, key, value,
    key_hint=None, value_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Puts a value with a given key to cache only if the key does not
    already exist.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param value: value for the key,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param value_hint: (optional) Ignite data type, for which the given value
     should be converted.
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and an old value
     or None on success, non-zero status and an error description otherwise.
    """

    class CacheGetAndPutIfAbsentQuery(Query):
        op_code = OP_CACHE_GET_AND_PUT_IF_ABSENT

    query_struct = CacheGetAndPutIfAbsentQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
        ('value', value_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
        'value': value,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('value', AnyDataObject),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['value']
    return result


def cache_replace(
    conn: Connection, hash_code: int, key, value,
    key_hint=None, value_hint=None, binary=False, query_id=None,
) -> APIResult:
    """
    Puts a value with a given key to cache only if the key already exist.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key: key for the cache entry. Can be of any supported type,
    :param value: value for the key,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param value_hint: (optional) Ignite data type, for which the given value
     should be converted.
    :param binary: pass True to keep the value in binary form. False
     by default,
    :param query_id: a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status and a boolean
     success code, or non-zero status and an error description if something
     has gone wrong.
    """

    class CacheReplaceQuery(Query):
        op_code = OP_CACHE_REPLACE

    query_struct = CacheReplaceQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
        ('value', value_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
        'value': value,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('success', Bool),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['success']
    return result


def cache_replace_if_equals(
    conn: Connection, hash_code: int, key, sample, value,
    key_hint=None, sample_hint=None, value_hint=None,
    binary=False, query_id=None,
) -> APIResult:
    """
    Puts a value with a given key to cache only if the key already exists
    and value equals provided sample.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key:  key for the cache entry,
    :param sample: a sample to compare the stored value with,
    :param value: new value for the given key,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param sample_hint: (optional) Ignite data type, for whic
     the given sample should be converted
    :param value_hint: (optional) Ignite data type, for which the given value
     should be converted,
    :param binary: (optional) pass True to keep the value in binary form.
     False by default,
    :param query_id: (optional) a value generated by client and returned
     as-is in response.query_id. When the parameter is omitted, a random
     value is generated,
    :return: API result data object. Contains zero status and a boolean
     success code, or non-zero status and an error description if something
     has gone wrong.
    """

    class CacheReplaceIfEqualsQuery(Query):
        op_code = OP_CACHE_REPLACE_IF_EQUALS

    query_struct = CacheReplaceIfEqualsQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
        ('sample', sample_hint or AnyDataObject),
        ('value', value_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
        'sample': sample,
        'value': value,
    })

    conn.send(send_buffer)

    response_struct = Response([
        ('success', Bool),
    ])
    response_class, recv_buffer = response_struct.parse(conn)
    response = response_class.from_buffer_copy(recv_buffer)

    result = APIResult(
        status=response.status_code,
        query_id=response.query_id,
    )
    if hasattr(response, 'error_message'):
        result.message = response.error_message
    result.value = response_struct.to_python(response)['success']
    return result


def cache_clear(
    conn: Connection, hash_code: int, binary=False, query_id=None,
) -> APIResult:
    """
    Clears the cache without notifying listeners or cache writers.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param binary: (optional) pass True to keep the value in binary form.
     False by default,
    :param query_id: (optional) a value generated by client and returned
     as-is in response.query_id. When the parameter is omitted, a random
     value is generated,
    :return: API result data object. Contains zero status on success,
     non-zero status and an error description otherwise.
    """

    class CacheClearQuery(Query):
        op_code = OP_CACHE_CLEAR

    query_struct = CacheClearQuery([
        ('hash_code', Int),
        ('flag', Byte),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
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


def cache_clear_key(
    conn: Connection, hash_code: int, key,
    key_hint: object=None, binary=False, query_id=None,
) -> APIResult:
    """
    Clears the cache key without notifying listeners or cache writers.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param key:  key for the cache entry,
    :param key_hint: (optional) Ignite data type, for which the given key
     should be converted,
    :param binary: (optional) pass True to keep the value in binary form.
     False by default,
    :param query_id: (optional) a value generated by client and returned
     as-is in response.query_id. When the parameter is omitted, a random
     value is generated,
    :return: API result data object. Contains zero status on success,
     non-zero status and an error description otherwise.
    """

    class CacheClearKeyQuery(Query):
        op_code = OP_CACHE_CLEAR_KEY

    query_struct = CacheClearKeyQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('key', key_hint or AnyDataObject),
    ], query_id=query_id)

    _, send_buffer = query_struct.from_python({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'key': key,
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


def cache_clear_keys(
    conn: Connection, hash_code: int, keys: list, binary=False, query_id=None,
) -> APIResult:
    """
    Clears the cache keys without notifying listeners or cache writers.

    :param conn: connection to Ignite server,
    :param hash_code: hash code of the cache. Can be obtained by applying
     the `hashcode()` function to the cache name,
    :param keys: list of keys or tuples of (key, key_hint),
    :param binary: (optional) pass True to keep the value in binary form.
     False by default,
    :param query_id: (optional) a value generated by client and returned as-is
     in response.query_id. When the parameter is omitted, a random value
     is generated,
    :return: API result data object. Contains zero status on success,
     non-zero status and an error description otherwise.
    """

    class CacheClearKeysQuery(Query):
        op_code = OP_CACHE_CLEAR_KEYS

    value_hint_pairs = []
    length = len(keys)
    for key_or_pair in keys:
        if is_hinted(key_or_pair):
            value_hint_pairs.append(key_or_pair)
        else:
            value_hint_pairs.append((key_or_pair, AnyDataObject))

    # structure name: hint
    key_fields = {}
    # structure name: value
    data = {}
    for i, pair in enumerate(value_hint_pairs):
        name = 'element_{}'.format(i)
        value, hint = pair
        key_fields[name] = hint
        data[name] = value

    query_struct = CacheClearKeysQuery([
        ('hash_code', Int),
        ('flag', Byte),
        ('length', Int),
    ] + list(key_fields.items()), query_id=query_id)

    data.update({
        'hash_code': hash_code,
        'flag': 1 if binary else 0,
        'length': length,
    })
    _, send_buffer = query_struct.from_python(data)
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
