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

from decimal import Decimal
import socket

from datatypes.class_configs import *
from datatypes.type_codes import *
from .null import null_class, null_object
from .simple import simple_data_class, simple_data_object
from .standard import standard_data_class, standard_data_object
from .string import string_class, string_object
from .fractional import fractional_class, fractional_object
from .arrays import array_data_class, array_data_object
from .vararrays import vararray_data_class, vararray_data_object


NoneType = type(None)


ITER_TYPE_NON_ITERABLE = 0
ITER_TYPE_HETEROGENEOUS = 1
ITER_TYPE_VARIABLE_LENGTH = 2
ITER_TYPE_UNIFORM = 3


def iter_type(var):
    try:
        iter_var = iter(var)
    except TypeError:
        return ITER_TYPE_NON_ITERABLE
    first_type = type(iter_var.__next__())
    if all([type(x) == first_type for x in iter_var]):
        if first_type in vararray_types:
            return ITER_TYPE_VARIABLE_LENGTH
        return ITER_TYPE_UNIFORM
    return ITER_TYPE_HETEROGENEOUS


def data_class(python_var, tc_hint, **kwargs):
    """
    Dispatcher function for data class creation functions.

    :param python_var: variable of native Python type to be converted
    to DataObject. The choice of data class depends on its type.
    If None, tc_hint is used,
    :param tc_hint: direct indicator of required data class type,
    :param kwargs: data class-specific arguments,
    :return: data class.
    """
    python_type = type(python_var)

    if python_type is NoneType and tc_hint is None:
        return null_class()

    if python_type in simple_python_types or (
        python_type is NoneType and tc_hint in simple_types
    ):
        return simple_data_class(python_var, tc_hint=tc_hint, **kwargs)

    if python_type in (str, bytes) or (
        python_type is NoneType and tc_hint == TC_STRING
    ):
        return string_class(python_var, tc_hint=tc_hint, **kwargs)

    if python_type in standard_python_types or (
        python_type is NoneType and tc_hint in standard_types
    ):
        return standard_data_class(python_var, tc_hint=tc_hint, **kwargs)

    if python_type is Decimal or (
        python_type is NoneType and tc_hint == TC_DECIMAL
    ):
        return fractional_class(python_var, tc_hint=tc_hint, **kwargs)

    if iter_type(python_type) == ITER_TYPE_UNIFORM or (
        python_type is NoneType and tc_hint in array_types
    ):
        return array_data_class(python_var, tc_hint=tc_hint, **kwargs)

    if iter_type(python_type) == ITER_TYPE_VARIABLE_LENGTH or (
        python_type is NoneType and tc_hint in vararray_types
    ):
        return vararray_data_class(python_var, tc_hint=tc_hint, **kwargs)

    else:
        raise NotImplementedError('This data type is not supported.')


def data_object(connection: socket.socket, initial=None, **kwargs):
    """
    Dispatcher function for parsing binary stream into data objects.

    :param connection: socket.socket-compatible data stream,
    :param initial: already received data,
    :return: data object.
    """
    initial = initial or connection.recv(1)

    if initial == TC_NULL:
        return null_object(connection, initial=initial, **kwargs)
    if initial in simple_types:
        return simple_data_object(connection, initial=initial, **kwargs)
    if initial == TC_STRING:
        return string_object(connection, initial=initial, **kwargs)
    if initial in standard_types:
        return standard_data_object(connection, initial=initial, **kwargs)
    if initial == TC_DECIMAL:
        return fractional_object(connection, initial=initial, **kwargs)
    if initial in array_types:
        return array_data_object(connection, initial=initial, **kwargs)
    if initial in vararray_types:
        return vararray_data_object(connection, initial=initial, **kwargs)
    raise NotImplementedError('This data type is not supported.')
