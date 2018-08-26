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

from collections import OrderedDict
from decimal import Decimal

from pyignite.client.binary import GenericObjectMeta
from pyignite.datatypes import (
    BinaryObject, BoolObject, IntObject, DecimalObject, LongObject, String,
)
from pyignite.datatypes.prop_codes import *


insert_data = [
    [1, True, 'asdf', 42, Decimal('2.4')],
    [2, False, 'zxcvb', 43, Decimal('2.5')],
    [3, True, 'qwerty', 44, Decimal('2.6')],
]

page_size = 100

scheme_name = 'PUBLIC'

table_sql_name = 'AllDataType'
table_cache_name = 'SQL_{}_{}'.format(
    scheme_name,
    table_sql_name.upper(),
)

create_query = '''
CREATE TABLE {} (
  test_pk INTEGER(11) PRIMARY KEY,
  test_bool BOOLEAN,
  test_str VARCHAR(24),
  test_int INTEGER(11),
  test_decimal DECIMAL(11, 5),
)
'''.format(table_sql_name)

insert_query = '''
INSERT INTO {} (
  test_pk, test_bool, test_str, test_int, test_decimal, 
) VALUES (?, ?, ?, ?, ?)'''.format(table_sql_name)

select_query = '''SELECT * FROM {}'''.format(table_sql_name)

drop_query = 'DROP TABLE {} IF EXISTS'.format(table_sql_name)


def test_sql_read_as_binary(client):

    client.sql(drop_query)

    # create table
    client.sql(create_query)

    # insert some rows
    for line in insert_data:
        client.sql(insert_query, query_args=line)

    table_cache = client.get_cache(table_cache_name)
    result = table_cache.scan()

    # convert Binary object fields' values to a tuple
    # to compare it with the initial data
    for key, value in result:
        assert key in {x[0] for x in insert_data}
        assert (
                   value.TEST_BOOL,
                   value.TEST_STR,
                   value.TEST_INT,
                   value.TEST_DECIMAL
               ) in {tuple(x[1:]) for x in insert_data}

    client.sql(drop_query)


def test_sql_write_as_binary(client):

    client.get_or_create_cache(scheme_name)

    # configure cache as an SQL table
    type_name = table_cache_name

    # register binary type
    class AllDataType(
        metaclass=GenericObjectMeta,
        type_name=type_name,
        schema=OrderedDict([
            ('TEST_BOOL', BoolObject),
            ('TEST_STR', String),
            ('TEST_INT', IntObject),
            ('TEST_DECIMAL', DecimalObject),
        ]),
    ):
        pass

    table_cache = client.get_or_create_cache({
        PROP_NAME: table_cache_name,
        PROP_SQL_SCHEMA: scheme_name,
        PROP_QUERY_ENTITIES: [
            {
                'table_name': table_sql_name.upper(),
                'key_field_name': 'TEST_PK',
                'key_type_name': 'java.lang.Integer',
                'field_name_aliases': [],
                'query_fields': [
                    {
                        'name': 'TEST_PK',
                        'type_name': 'java.lang.Integer',
                        'is_key_field': True,
                        'is_notnull_constraint_field': True,
                        'default_value': None,
                    },
                    {
                        'name': 'TEST_BOOL',
                        'type_name': 'java.lang.Boolean',
                        'is_key_field': False,
                        'is_notnull_constraint_field': False,
                        'default_value': None,
                    },
                    {
                        'name': 'TEST_STR',
                        'type_name': 'java.lang.String',
                        'is_key_field': False,
                        'is_notnull_constraint_field': False,
                        'default_value': None,
                    },
                    {
                        'name': 'TEST_INT',
                        'type_name': 'java.lang.Integer',
                        'is_key_field': False,
                        'is_notnull_constraint_field': False,
                        'default_value': None,
                    },
                    {
                        'name': 'TEST_DECIMAL',
                        'type_name': 'java.math.BigDecimal',
                        'is_key_field': False,
                        'is_notnull_constraint_field': False,
                        'default_value': None,
                    },
                ],
                'query_indexes': [],
                'value_type_name': type_name,
                'value_field_name': None,
            },
        ],
    })
    table_settings = table_cache.settings
    assert table_settings, 'SQL table cache settings are empty'

    client.put_binary_type(data_class=AllDataType)

    # insert rows as k-v
    for row in insert_data:
        value = AllDataType()
        setattr(value, 'TEST_BOOL', row[1])
        setattr(value, 'TEST_STR', row[2])
        setattr(value, 'TEST_INT', row[3])
        setattr(value, 'TEST_DECIMAL', row[4])
        table_cache.put(row[0], value, key_hint=IntObject)

    data = table_cache.scan()
    assert len(list(data)) == len(insert_data), (
        'Not all data was read as key-value'
    )

    # read rows as SQL
    data = client.sql(select_query, include_field_names=True)

    header_row = next(data)
    for field_name in AllDataType.schema.keys():
        assert field_name in header_row, 'Not all field names in header row'

    data = list(data)
    assert len(data) == len(insert_data), 'Not all data was read as SQL rows'

    # cleanup
    table_cache.destroy()


def test_nested_binary_objects(client):

    nested_cache = client.get_or_create_cache('nested_binary')

    class InnerType(
        metaclass=GenericObjectMeta,
        schema=OrderedDict([
            ('inner_int', LongObject),
            ('inner_str', String),
        ]),
    ):
        pass

    class OuterType(
        metaclass=GenericObjectMeta,
        schema=OrderedDict([
            ('outer_int', LongObject),
            ('nested_binary', BinaryObject),
            ('outer_str', String),
        ]),
    ):
        pass

    client.put_binary_type(data_class=InnerType)
    client.put_binary_type(data_class=OuterType)

    inner = InnerType()
    inner.inner_int = 42
    inner.inner_str = 'This is a test string'

    outer = OuterType()
    outer.outer_int = 43
    outer.nested_binary = inner
    outer.outer_str = 'This is another test string'

    nested_cache.put(1, outer)

    result = nested_cache.get(1)
    assert result.outer_int == 43
    assert result.outer_str == 'This is another test string'
    assert result.nested_binary.inner_int == 42
    assert result.nested_binary.inner_str == 'This is a test string'

    nested_cache.destroy()


def test_add_schema_to_binary_object(client):

    migrate_cache = client.create_cache('migrate_binary')

    class MyBinaryType(
        metaclass=GenericObjectMeta,
        schema=OrderedDict([
            ('test_str', String),
            ('test_int', LongObject),
            ('test_bool', BoolObject),
        ]),
    ):
        pass

    client.put_binary_type(data_class=MyBinaryType)

    binary_object = MyBinaryType()
    binary_object.test_str = 'Test string'
    binary_object.test_int = 42
    binary_object.test_bool = True

    migrate_cache.put(1, binary_object)

    result = migrate_cache.get(1)
    assert result.test_str == 'Test string'
    assert result.test_int == 42
    assert result.test_bool is True

    modified_schema = MyBinaryType.schema.copy()
    modified_schema['test_decimal'] = DecimalObject
    del modified_schema['test_bool']

    class MyBinaryTypeV2(
        metaclass=GenericObjectMeta,
        type_name='MyBinaryType',
        schema=modified_schema,
    ):
        pass

    client.put_binary_type(data_class=MyBinaryTypeV2)
    assert MyBinaryType.type_id == MyBinaryTypeV2.type_id
    assert MyBinaryType.schema_id != MyBinaryTypeV2.schema_id

    binary_object_v2 = MyBinaryTypeV2()
    binary_object_v2.test_str = 'Another test'
    binary_object_v2.test_int = 43
    binary_object_v2.test_decimal = Decimal('2.34')

    migrate_cache.put(2, binary_object_v2)

    result = migrate_cache.get(2)
    assert result.test_str == 'Another test'
    assert result.test_int == 43
    assert result.test_decimal == Decimal('2.34')
    assert not hasattr(result, 'test_bool')

    migrate_cache.destroy()
