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

import ctypes

from pyignite.constants import *
from .base import IgniteDataType
from .type_ids import *


__all__ = [
    'Primitive',
    'Byte', 'Short', 'Int', 'Long', 'Float', 'Double', 'Char', 'Bool',
]


class Primitive(IgniteDataType):
    """
    Ignite primitive type. Base type for the following types:

    - Byte,
    - Short,
    - Int,
    - Long,
    - Float,
    - Double,
    - Char,
    - Bool.
    """
    _type_name = None
    _type_id = None
    c_type = None

    @classmethod
    def parse(cls, client: 'Client'):
        return cls.c_type, client.recv(ctypes.sizeof(cls.c_type))

    @staticmethod
    def to_python(ctype_object, *args, **kwargs):
        return ctype_object

    @classmethod
    def from_python(cls, value):
        return bytes(cls.c_type(value))


class Byte(Primitive):
    _type_name = 'java.lang.Byte'
    _type_id = TYPE_BYTE
    c_type = ctypes.c_byte


class Short(Primitive):
    _type_name = 'java.lang.Short'
    _type_id = TYPE_SHORT
    c_type = ctypes.c_short


class Int(Primitive):
    _type_name = 'java.lang.Integer'
    _type_id = TYPE_INT
    c_type = ctypes.c_int


class Long(Primitive):
    _type_name = 'java.lang.Long'
    _type_id = TYPE_LONG
    c_type = ctypes.c_longlong


class Float(Primitive):
    _type_name = 'java.lang.Float'
    _type_id = TYPE_FLOAT
    c_type = ctypes.c_float


class Double(Primitive):
    _type_name = 'java.lang.Double'
    _type_id = TYPE_DOUBLE
    c_type = ctypes.c_double


class Char(Primitive):
    _type_name = 'java.lang.Character'
    _type_id = TYPE_CHAR
    c_type = ctypes.c_short

    @classmethod
    def to_python(cls, ctype_object, *args, **kwargs):
        return ctype_object.value.to_bytes(
            ctypes.sizeof(cls.c_type),
            byteorder=PROTOCOL_BYTE_ORDER
        ).decode(PROTOCOL_CHAR_ENCODING)

    @classmethod
    def from_python(cls, value):
        if type(value) is str:
            value = value.encode(PROTOCOL_CHAR_ENCODING)
        # assuming either a bytes or an integer
        if type(value) is bytes:
            value = int.from_bytes(value, byteorder=PROTOCOL_BYTE_ORDER)
        # assuming a valid integer
        return value.to_bytes(
            ctypes.sizeof(cls.c_type),
            byteorder=PROTOCOL_BYTE_ORDER
        )


class Bool(Primitive):
    _type_name = 'java.lang.Boolean'
    _type_id = TYPE_BOOLEAN
    c_type = ctypes.c_bool
