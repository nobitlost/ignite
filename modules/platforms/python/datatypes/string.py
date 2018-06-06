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
UTF-8-encoded human-readable strings.
"""

import ctypes
import socket

from .type_codes import *
from .simple import init
from constants import *


def string_get_attribute(self):
    try:
        return self.data.decode(PROTOCOL_STRING_ENCODING)
    except UnicodeDecodeError:
        return self.data


def string_set_attribute(self, value):
    # warning: no length check is done on this stage
    if type(value) is bytes:
        self.data = value
    else:
        self.data = bytes(value, encoding='utf-8')


def string_class(python_var, length=None, **kwargs):
    # python_var is of type str or bytes
    if type(python_var) is bytes:
        length = len(python_var)
    elif python_var is not None:
        length = len(bytes(python_var, encoding=PROTOCOL_STRING_ENCODING))
    return type(
        'String',
        (ctypes.LittleEndianStructure,),
        {
            '_pack_': 1,
            '_fields_': [
                ('type_code', ctypes.c_byte),
                ('length', ctypes.c_int),
                ('data', ctypes.c_char * length),
            ],
            '_type_code': TC_STRING,
            'init': init,
            'get_attribute': string_get_attribute,
            'set_attribute': string_set_attribute,
        },
    )


def string_object(connection: socket.socket, initial=None):
    buffer = initial or connection.recv(1)
    type_code = buffer
    assert type_code == TC_STRING, 'Can not create string: wrong type code.'
    length_buffer = connection.recv(4)
    length = int.from_bytes(length_buffer, byteorder='little')
    data_class = string_class(None, length)
    buffer += length_buffer + connection.recv(length)
    data_object = data_class.from_buffer_copy(buffer)
    return data_object
