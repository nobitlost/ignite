# PHP Thin Client #

## Overview ##

This thin client allows your PHP applications to work with Apache Ignite clusters via [Binary Client Protocol](https://apacheignite.readme.io/v2.6/docs/binary-client-protocol).

A thin client is a lightweight Ignite client that connects to the cluster via a standard socket connection. It does not start in JVM process (Java is not required at all), does not become a part of the cluster topology, never holds any data or used as a destination of compute grid calculations.

What it does is it simply establishes a socket connection to a standard Ignite node and performs all operations through that node.

## Prerequisites ##

The client requires PHP version 7.2 or higher (http://php.net/manual/en/install.php) and Composer Dependency Manager (https://getcomposer.org/download/).

The client additionally requires PHP Multibyte String extension. Depending on you PHP configuration you may need to additionally install/configure it (http://php.net/manual/en/mbstring.installation.php)

The client has been tested on the following platforms:
- Ubuntu 14.04 LTS 32-bit
- Ubuntu 14.04 LTS 64-bit
- Windows 10 Home 64-bit

Before connecting to Ignite from PHP thin client, start at least one Ignite cluster node. For instance, you can use `ignite.sh` script as follows:

In Unix:
```bash
./ignite.sh
```

In Windows:
```bash
ignite.bat
```

## Quick Start ##

Let's use existing [PHP examples](#full-examples) that are delivered with every Ignite distribution for the sake of quick getting started.

1. [Prerequisites](#prerequisites)

2. [Install the examples](#examples-installation)

3. [Setup and run examples](#examples-setup-and-running)

4. [Examples description](#examples-description)

## Supported APIs ##

The client API specification can be found [here](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/index.html).

The client supports all operations and types from the [Binary Client Protocol v.2.6](https://apacheignite.readme.io/v2.6/docs/binary-client-protocol) except the following not-applicable features:
- OP_REGISTER_BINARY_TYPE_NAME and OP_GET_BINARY_TYPE_NAME operations are not supported.
- Filter object for OP_QUERY_SCAN operation is not supported. OP_QUERY_SCAN operation itself is supported.
- It is not possible to register a new Ignite Enum type. Reading and writing items of the existing Ignite Enum types are supported.

The following additional features are supported:
- SSL/TLS connection.
- "Failover re-connection algorithm".

All API method calls are synchronous.

## Data Types ##

A mapping between Ignite types defined by the Binary Client Protocol and PHP types occurs every time an application writes or reads a field to/from an Ignite via the client's API. The field here is any data stored in Ignite - the whole key or value of an Ignite entry, an element of an array or set, a field of a complex object, etc.

The client supports two cases of mapping:
- default mapping,
- explicit mapping.

### Default Mapping ###

Default mapping between Ignite and PHP types is described [here](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_type_1_1_object_type.html). It defines what happens if an application does not use the explicit type mapping for a field.

### Explicit Mapping ###

Using the client's API methods, an application can explicitly specify an Ignite type for a particular field. The client uses this information to transform the field from PHP type to Ignite type and vice verse during the read/write operations.

If an application does not explicitly specify an Ignite type for a field, the client uses default mapping during the field read/write operations.

### Complex Object Type Support ###

The client provides two ways to operate with Ignite Complex Object type - in the deserialized form and the binary form.

An application can specify an Ignite type of a field by an instance of the [ComplexObjectType](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_type_1_1_complex_object_type.html) class which references a PHP class. In this case, when the application reads a value of the field, the client deserializes the received Ignite Complex Object and returns it to the client as an instance of the referenced PHP class. When the application writes a value of the field, the client expects an instance of the referenced PHP class and serializes it to the Ignite Complex Object.

If an application does not specify an Ignite type of a field and reads a value of the field, the client returns the received Ignite Complex Object as an instance of the [BinaryObject](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_data_1_1_binary_object.html) class - a binary form of the Ignite Complex Object. The `BinaryObject` allows working with its content (read and write values of the object's fields, add and remove the fields, etc.) avoiding deserialization. Also, the application can create an instance of the `BinaryObject` class from a PHP object. An application can write the `BinaryObject` as a value of a field into Ignite, if that field has no explicitly specified Ignite type.

The client takes care of obtaining or registering information about Ignite Complex Object type, including schema, from/at Ignite cluster. It is done automatically by the client, when required for reading or writing of the Ignite Complex Object from/to Ignite.

## Usage ##

The below sections explain the basic steps to work with Apache Ignite using PHP client.

See the [Prerequisites](#prerequisites) section first.

## Installation ##

### Installation from the PHP Package Repository ###

Run from your application root
```
composer require apache/apache-ignite-client
```

To use the client in your application, include `vendor/autoload.php` file, generated by Composer, to your source code, eg.
```
require_once __DIR__ . '/vendor/autoload.php';
```

### Installation from Sources ###

1. Clone or download the Ignite repository to `local_ignite_path`
2. Go to `local_ignite_path/modules/platforms/php` folder
3. Execute `composer install --no-dev` command

```bash
cd local_ignite_path/modules/platforms/php
composer install --no-dev
```

To use the client in your application, include `vendor/autoload.php` file, generated by Composer, to your source code, eg.
```
require_once "<local_ignite_path>/vendor/autoload.php";
```

### Instantiating Ignite Client ###

A usage of the client starts with the creation of a [Client](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_client.html) object that connects a PHP application to the cluster.

It is possible to create as many `Client` objects as needed. All of them will work independently.

```
use Apache\Ignite\Client;

$client = new Client();
```

### Configuring Ignite Client ###

The next step is to define a configuration for the client's connection by populating [ClientConfiguration](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_client_configuration.html) object.

A mandatory part of the configuration, which is specified in the constructor, is a list of endpoints of the Ignite nodes. At least one endpoint must be specified. A client connects to one node only - a random endpoint from the provided list. Other nodes, if provided, are used by the client for the "failover re-connection algorithm": the client tries to re-connect to the next random endpoint from the list if the current connection is lost.

Optional parts of the configuration can be specified using additional methods which include:
- Authentication using username/password.
- SSL/TLS connection.
- PHP connection options.

By default, the client establishes a non-secure connection with default connection options and does not use authentication.

The example below shows how to configure the client:

```
use Apache\Ignite\ClientConfiguration;

$clientConfiguration = new ClientConfiguration('127.0.0.1:10800');
```

The next example shows how to prepare Ignite Client Configuration with username/password authentication and additional connection options:

```
use Apache\Ignite\ClientConfiguration;

$clientConfiguration = (new ClientConfiguration('127.0.0.1:10800'))->
    setUserName('ignite')->
    setPassword('ignite')->
    setTimeout(5000);
```

### Connecting to the Cluster ###

The next step is to connect the client to an Ignite cluster. The configuration for the client's connection, which includes endpoint(s) to connect to, is specified in the connect method.

If the client is not connected (including the case it can not successfully reconnect using the "failover re-connection algorithm"), the [NoConnectionException](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_exception_1_1_no_connection_exception.html) is thrown for any operation with the Ignite cluster.

If the client unexpectedly losts the connection before or during an operation, the [OperationStatusUnknownException](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_exception_1_1_operation_status_unknown_exception.html) is thrown. In this case, it is not known if the operation has been actually executed in the cluster or not. Note, the "failover re-connection algorithm" will be executed when the next operation is called by the application.

At any moment, an application can forcibly disconnect the client by calling the disconnect method.

When the client becomes disconnected, an application can call the connect method again - with the same or different configuration (eg. with a different list of endpoints).

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Exception\ClientException;

function connectClient(): void
{
    $client = new Client();
    try {
        $clientConfiguration = new ClientConfiguration(
            '127.0.0.1:10800', '127.0.0.1:10801', '127.0.0.1:10802');
        // connect to Ignite node
        $client->connect($clientConfiguration);
    } catch (ClientException $e) {
        echo($e->getMessage());
    }
}

connectClient();
```

### Caches Usage and Configuration ###

The next step is to obtain an object representing an Ignite cache. It's an instance of a PHP class with the [CacheInterface](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/interface_apache_1_1_ignite_1_1_cache_1_1_cache_interface.html).

The thin client provides several methods to work with Ignite caches and to obtain objects with the `CacheInterface` - get a cache by its name, create a cache with a specified name and optional cache configuration, get or create a cache, destroys a cache, etc.

It is possible to obtain as many objects with the `CacheInterface` as needed - for the same or different Ignite caches - and work with all of them in parallel.

The following example shows how to get access to a cache by name and destroy its later:

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Exception\ClientException;

function getOrCreateCacheByName(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        // get or create cache by name
        $cache = $client->getOrCreateCache('myCache');

        // perform cache key-value operations
        // ...

        // destroy cache
        $client->destroyCache('myCache');
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

getOrCreateCacheByName();
```

The next example shows how to get access to a cache by name and with a configuration:

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Cache\CacheConfiguration;
use Apache\Ignite\Exception\ClientException;

function createCacheByConfiguration(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        // create cache by name and configuration
        $cache = $client->createCache(
            'myCache',
            (new CacheConfiguration())->setSqlSchema('PUBLIC'));
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

createCacheByConfiguration();
```

This example shows how to get an existing cache by name:

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Cache\CacheConfiguration;
use Apache\Ignite\Exception\ClientException;

function getExistingCache(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        // create cache by name and configuration
        $cache = $client->getCache('myCache');
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

getExistingCache();
```

### Types Mapping Configuration ###

The next step is optional.

It is possible to specify concrete Ignite types for the key and/or the value of the cache. If the key and/or value is a non-primitive type (eg. a map, a collection, a complex object, etc.) it is possible to specify concrete Ignite types for fields of that objects as well.

If Ignite type is not explicitly specified for some field, the client tries to make automatic default mapping between PHP types and Ignite object types.

More details about types and mappings are clarified in the [Data Types](#data-types) section.

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Type\MapObjectType;
use Apache\Ignite\Exception\ClientException;

function setCacheKeyValueTypes(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        $cache = $client->getOrCreateCache('myCache');
        $cache->setKeyType(ObjectType::INTEGER)->
            setValueType(new MapObjectType(
                MapObjectType::LINKED_HASH_MAP,
                ObjectType::SHORT,
                ObjectType::BYTE_ARRAY));
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

setCacheKeyValueTypes();
```

At this point, we're ready to start working with the data stored or to be placed in Ignite.

### Key-Value Queries ###

The `CacheInterface` provides methods to work with the key and the value of the cache using Key-Value operations - put, get, put all, get all, replace and others. This example shows how to do that:

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Cache\CacheEntry;
use Apache\Ignite\Exception\ClientException;

function performCacheKeyValueOperations(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        $cache = $client->getOrCreateCache('myCache')->
            setKeyType(ObjectType::INTEGER);
        
        // put and get value
        $cache->put(1, 'abc');
        $value = $cache->get(1);

        // put and get multiple values using putAll()/getAll() methods
        $cache->putAll([new CacheEntry(2, 'value2'), new CacheEntry(3, 'value3')]);
        $values = $cache->getAll([1, 2, 3]);

        // removes all entries from the cache
        $cache->clear();
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

performCacheKeyValueOperations();
```

Now, let's see how to put/get Complex Objects and Binary Objects:

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Type\ComplexObjectType;
use Apache\Ignite\Exception\ClientException;

class Person
{
    public $id;
    public $name;
    public $salary;
            
    public function __construct(int $id = 0, string $name = null, float $salary = 0)
    {
        $this->id = $id;
        $this->name = $name;
        $this->salary = $salary;
    }
}

function putGetComplexAndBinaryObjects(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        $cache = $client->getOrCreateCache('myPersonCache')->
            setKeyType(ObjectType::INTEGER);
        // Complex Object type for PHP Person class instances
        $personComplexObjectType = (new ComplexObjectType())->
            setFieldType('id', ObjectType::INTEGER); 
        // set cache key and value types
        $cache->setKeyType(ObjectType::INTEGER)->
            setValueType($personComplexObjectType);
        // put Complex Objects to the cache
        $cache->put(1, new Person(1, 'John Doe', 1000));
        $cache->put(2, new Person(2, 'Jane Roe', 2000));
        // get Complex Object, returned value is an instance of Person class
        $person = $cache->get(1);
        print_r($person);

        // new CacheClient instance of the same cache to operate with BinaryObjects
        $binaryCache = $client->getCache('myPersonCache')->
            setKeyType(ObjectType::INTEGER);
        // get Complex Object from the cache in a binary form, returned value is an instance of BinaryObject class
        $binaryPerson = $binaryCache->get(2);
        echo('Binary form of Person:' . PHP_EOL);
        foreach ($binaryPerson->getFieldNames() as $fieldName) {
            $fieldValue = $binaryPerson->getField($fieldName);
            echo($fieldName . ' : ' . $fieldValue . PHP_EOL);
        }
        // modify Binary Object and put it to the cache
        $binaryPerson->setField('id', 3, ObjectType::INTEGER)->
            setField('name', 'Mary Major');
        $binaryCache->put(3, $binaryPerson);

        // get Binary Object from the cache and convert it to PHP object
        $binaryPerson = $binaryCache->get(3);
        print_r($binaryPerson->toObject($personComplexObjectType));

        $client->destroyCache('myPersonCache');
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

putGetComplexAndBinaryObjects();
```

### SQL and Scan Queries ###

PHP client supports Ignite SQL and scan queries. A query method returns a cursor object with the standard PHP Iterator interface which allows to iterate over the set with the query results lazily, one by one. Additionally, the cursor has methods to get the whole results at once.

#### Scan Query ####

First, define the query by creating and configuring an instance of the [ScanQuery](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_query_1_1_scan_query.html) class.

Then, pass the `ScanQuery` instance to the query method of the `CacheInterface`.

Finally, use the returned object with the [CursorInterface](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/interface_apache_1_1_ignite_1_1_query_1_1_cursor_interface.html) to iterate over or get all cache entries returned by the query.

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Cache\CacheEntry;
use Apache\Ignite\Query\ScanQuery;
use Apache\Ignite\Exception\ClientException;

function performScanQuery(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        $cache = $client->getOrCreateCache('myCache')->
            setKeyType(ObjectType::INTEGER);
        
        // put multiple values using putAll()
        $cache->putAll([
            new CacheEntry(1, 'value1'),
            new CacheEntry(2, 'value2'), 
            new CacheEntry(3, 'value3')]);
        
        // create and configure scan query
        $scanQuery = (new ScanQuery())->
            setPageSize(1);
        // obtain scan query cursor
        $cursor = $cache->query($scanQuery);
        // getAll cache entries returned by the scan query
        foreach ($cursor->getAll() as $cacheEntry) {
            echo($cacheEntry->getValue() . PHP_EOL);
        }
        
        $client->destroyCache('myCache');
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

performScanQuery();
```

#### SQL Query ####

First, define the query by creating and configuring an instance of the [SqlQuery](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_query_1_1_sql_query.html) class.

Then, pass the `SqlQuery` instance to the query method of the `CacheInterface`.

Finally, use the returned object with the [CursorInterface](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/interface_apache_1_1_ignite_1_1_query_1_1_cursor_interface.html) to iterate over or get all cache entries returned by the query.

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Cache\CacheConfiguration;
use Apache\Ignite\Cache\QueryEntity;
use Apache\Ignite\Cache\QueryField;
use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Type\ComplexObjectType;
use Apache\Ignite\Cache\CacheEntry;
use Apache\Ignite\Query\SqlQuery;
use Apache\Ignite\Exception\ClientException;

class Person
{
    public $name;
    public $salary;

    public function __construct(string $name = null, float $salary = 0)
    {
        $this->name = $name;
        $this->salary = $salary;
    }
}

function performSqlQuery(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        // cache configuration required for sql query execution
        $cacheConfiguration = (new CacheConfiguration())->
        setQueryEntities(
            (new QueryEntity())->
                setValueTypeName('Person')->
                setFields(
                    new QueryField('name', 'java.lang.String'),
                    new QueryField('salary', 'java.lang.Double')
                ));
        $cache = $client->getOrCreateCache('sqlQueryPersonCache', $cacheConfiguration)->
        setKeyType(ObjectType::INTEGER)->
        setValueType(new ComplexObjectType());

        // put multiple values using putAll()
        $cache->putAll([
            new CacheEntry(1, new Person('John Doe', 1000)),
            new CacheEntry(2, new Person('Jane Roe', 2000)),
            new CacheEntry(2, new Person('Mary Major', 1500))]);

        // create and configure sql query
        $sqlQuery = (new SqlQuery('Person', 'salary > ? and salary <= ?'))->
            setArgs(900, 1600);
        // obtain sql query cursor
        $cursor = $cache->query($sqlQuery);
        // iterate over cache entries returned by the sql query
        foreach ($cursor as $cacheEntry) {
            print_r($cacheEntry->getValue());
        }

        $client->destroyCache('sqlQueryPersonCache');
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

performSqlQuery();
```

#### SQL Fields Query ####

This type of queries is used to obtain individual fields as a part of an SQL query result set, execute DML and DDL statements such as INSERT, UPDATE, DELETE, CREATE and other.

First, define the query by creating and configuring an instance of the [SqlFieldsQuery](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_query_1_1_sql_fields_query.html) class.

Then, pass the `SqlFieldsQuery` instance to the query method of the `CacheInterface`.

Finally, use the returned object with the [SqlFieldsCursorInterface](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/interface_apache_1_1_ignite_1_1_query_1_1_sql_fields_cursor_interface.html) to iterate over or get all elements returned by the query.

```
use Apache\Ignite\Client;
use Apache\Ignite\ClientConfiguration;
use Apache\Ignite\Cache\CacheConfiguration;
use Apache\Ignite\Type\ObjectType;
use Apache\Ignite\Query\SqlFieldsQuery;
use Apache\Ignite\Exception\ClientException;

function performSqlFieldsQuery(): void
{
    $client = new Client();
    try {
        $client->connect(new ClientConfiguration('127.0.0.1:10800'));
        $cache = $client->getOrCreateCache('myPersonCache', (new CacheConfiguration())->
        setSqlSchema('PUBLIC'));

        // create table using SqlFieldsQuery
        $cache->query(new SqlFieldsQuery(
            'CREATE TABLE Person (id INTEGER PRIMARY KEY, firstName VARCHAR, lastName VARCHAR, salary DOUBLE)'))->getAll();

        // insert data into the table
        $insertQuery = (new SqlFieldsQuery('INSERT INTO Person (id, firstName, lastName, salary) values (?, ?, ?, ?)'))->
            setArgTypes(ObjectType::INTEGER);
        $cache->query($insertQuery->setArgs(1, 'John', 'Doe', 1000))->getAll();
        $cache->query($insertQuery->setArgs(2, 'Jane', 'Roe', 2000))->getAll();

        // obtain sql fields cursor
        $sqlFieldsCursor = $cache->query(
            (new SqlFieldsQuery("SELECT concat(firstName, ' ', lastName), salary from Person"))->
                setPageSize(1));

        // iterate over elements returned by the query
        foreach ($sqlFieldsCursor as $fields) {
            print_r($fields);
        }

        // drop the table
        $cache->query(new SqlFieldsQuery("DROP TABLE Person"))->getAll();
    } catch (ClientException $e) {
        echo($e->getMessage());
    } finally {
        $client->disconnect();
    }
}

performSqlFieldsQuery();
```

### Errors Processing ###

Many of the client's methods throw PHP Exception in case of error.

There are three specific exceptions which may occur during the normal execution of an application. The application logic should process these errors:
- [OperationException](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_exception_1_1_operation_exception.html) - when the Ignite cluster returns an error for the requested operation.
- [NoConnectionException](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_exception_1_1_no_connection_exception.html) - when an operation with the Ignite cluster is called but the client is not connected to the cluster at this moment. The operation is not executed.
- [OperationStatusUnknownException](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_exception_1_1_operation_status_unknown_exception.html) - when an operation with the Ignite cluster is called and the client initiates it but a connection problem occurs during the operation. The status of the operation, whether it is executed or not in the Ignite cluster, is unknown.

Other errors (eg. wrong usage of the client, invalid arguments passed into methods, etc.) usually indicate issues during an application development which should be fixed during debugging and therefore should not occur after the application has been deployed. For all such errors the client throws the general exception:
- [ClientException](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_exception_1_1_client_exception.html)

```
try {
    // These exceptions are usually processed for a concrete operation    
    try {
        // Some operation with the Ignite cluster
        // ...
    } catch (OperationException $e) {
        // Ignite cluster returns an error, should be processed by an application's logic
    } catch (OperationStatusUnknownException $e) {
        // Status of the operation is unknown,
        // an application may repeat the operation if necessary
    }
    // ...
    
// These exceptions are usually processed for the whole application
} catch (NoConnectionException $e) {
    // The client is disconnected, all further operation with Ignite server fail till the client is connected again.
    // An application may recall connect() method with the same or different list of Ignite nodes.
} catch (ClientException $e) {
    // Usually means an issue that should be fixed during the development
}
```

### Enabling Debug ###

To switch on/off the client's debug output (including errors logging), call `setDebug()` method of the Ignite `Client` object. Debug output is disabled by default.

```
use Apache\Ignite\Client;

$client = new Client();
$client->setDebug(true);
```

---------------------------------------------------------------------

# Full Examples #

PHP Thin Client contains fully workable [examples](./examples) to demonstrate the main behavior of the client.

## Examples Installation ##

1. Clone or download the Ignite repository to `local_ignite_path`
2. Go to `local_ignite_path/modules/platforms/php` folder
3. Execute `composer install --no-dev` command

```bash
cd local_ignite_path/modules/platforms/php
composer install --no-dev
```

## Examples Setup and Running ##

1. Run Apache Ignite server - locally or remotely - if not run yet.

2. If needed, modify `ENDPOINT` constant in an example source file - Ignite node endpoint. The default value is `127.0.0.1:10800`.

3. Run an example by calling `php <example_file_name>.php`, eg:
```
cd {ignite}/modules/platforms/php/examples
php CachePutGetExample.php
```

## Examples Description ##

### Sql Example ###

Source: [SqlExample.php](./examples/SqlExample.php)

This example shows primary APIs to use with Ignite as with an SQL database:
- connects to a node
- creates a cache, if it doesn't exist
- creates tables (CREATE TABLE)
- creates indices (CREATE INDEX)
- writes data of primitive types into the tables (INSERT INTO table)
- reads data from the tables (SELECT ...)
- deletes tables (DROP TABLE)
- destroys the cache

### Cache Put Get Example ###

Source: [CachePutGetExample.php](./examples/CachePutGetExample.php)

This example demonstrates basic Cache, Key-Value Queries and Scan Query operations:
- connects to a node
- creates a cache, if it doesn't exist
  - specifies key type as Integer
- executes different cache operations with Complex Objects and Binary Objects
  - put several objects
  - putAll
  - get
  - getAll
  - ScanQuery
- destroys the cache

### Sql Query Entries Example ###

Source: [SqlQueryEntriesExample.php](./examples/SqlQueryEntriesExample.php)

This example demonstrates basic Cache, Key-Value Queries and SQL Query operations:
- connects to a node
- creates a cache from CacheConfiguration, if it doesn't exist
- writes data of primitive and Complex Object types into the cache using Key-Value put operation
- reads data from the cache using SQL Query
- destroys the cache

### Auth Tls Example ###

Source: [AuthTlsExample.php](./examples/AuthTlsExample.php)

This example requires [additional setup](#additional-setup-for-authtlsexample).

This example demonstrates how to establish a secure connection to an Ignite node and use username/password authentication, as well as basic Key-Value Queries operations for primitive types:
- connects to a node using TLS and providing username/password
- creates a cache, if it doesn't exist
  - specifies key and value type of the cache
- put data of primitive types into the cache
- get data from the cache
- destroys the cache

#### Additional Setup for AuthTlsExample ####

1. Obtain certificates required for TLS:
  - either use pre-generated certificates provided in the [examples/certs](./examples/certs) folder. Password for the files: `123456`. Note, these certificates work for an Ignite server installed locally only.
  - or obtain other existing certificates applicable for a concrete Ignite server.
  - or generate new certificates applicable for a concrete Ignite server.

  - The following files are needed:
    - keystore.jks, truststore.jks - for the server side
    - client.pem, ca.pem - for the client side

2. Place client.pem and ca.pem files somewhere locally, eg. into the [examples/certs](./examples/certs) folder.

3. If needed, modify `TLS_CLIENT_CERT_FILE_NAME` and `TLS_CA_FILE_NAME` constants in the example source file. The default values point to the files in the [examples/certs](./examples/certs) folder.

4. Setup Apache Ignite server to accept TLS - see appropriate Ignite documentation. Provide the obtained keystore.jks and truststore.jks certificates during the setup.

5. Switch on and setup authentication in Apache Ignite server - see appropriate Ignite documentation.

6. If needed, modify `USER_NAME` and `PASSWORD` constants in the example source file. The default values are the default Ignite username/password.

7. Executes [Setup and Running](#examples-setup-and-running) steps.

### Failover Example ###

Source: [FailoverExample.php](./examples/FailoverExample.php)

This example requires [additional setup](#additional-setup-for-failoverexample).

This example demonstrates "failover re-connection algorithm" of the client. It:
- configures the client to connect to a set of nodes
- connects to a node
- executes an operation with Ignite server in a cycle (10 operations with 5 seconds pause) and finishes (in about 50 seconds after start)
- if connection is broken, the client automatically tries to reconnect to another node
- if not possible to connect to any node, the example finishes immediately

#### Additional Setup for FailoverExample ####

1. Run three Ignite nodes. See appropriate Ignite documentation for more details.

2. If needed, modify `ENDPOINT1`, `ENDPOINT2`, `ENDPOINT2` constants in an example source file - Ignite node endpoints.
Default values are `localhost:10800`, `localhost:10801`, `localhost:10802` respectively.

2. Run the example by calling `php FailoverExample.php`. 

3. Shut down the node the client connected to (you can find it out from the client logs in the console).

4. From the logs, you will see that the client automatically reconnects to another node which is available.

5. Shut down all the nodes. You will see the client being stopped after failing to connect to each of the nodes.

Note, you have about 50 seconds after the example is started to play with the nodes. After this time the examples finishes.

---------------------------------------------------------------------

# Tests #

PHP Client for Apache Ignite contains [PHPUnit](https://phpunit.de/) tests to check the behavior of the client. The tests include:
- functional tests which cover all API methods of the client
- examples executors which run all examples except AuthTlsExample
- AuthTlsExample executor

The client has been tested on the following platforms:
- Ubuntu 14.04 LTS 32-bit
- Ubuntu 14.04 LTS 64-bit
- Windows 10 Home 64-bit

## Tests Installation ##

1. Clone or download Ignite repository the Ignite repository to `local_ignite_path`
2. Go to `local_ignite_path/modules/platforms/php` folder
3. Execute `composer install` command. Depending on you PHP configuration you may need to install/configure some additional PHP extensions required by PHPUnit (see Composer error messages if any).

```bash
cd local_ignite_path/modules/platforms/php
composer install
```

## Tests Running ##

1. Run Apache Ignite server locally or remotely with default configuration.
2. Set the environment variable:
    - **APACHE_IGNITE_CLIENT_ENDPOINTS** - comma separated list of Ignite node endpoints.
    - **APACHE_IGNITE_CLIENT_DEBUG** - (optional) if *true*, tests will display additional output (default: *false*).
3. Alternatively, instead of the environment variables setting, you can directly specify the values of the corresponding variables in [local_ignite_path/modules/platforms/php/tests/TestConfig.php](./tests/TestConfig.php) file.
4. Run the tests. 

The below commands include `--teamcity` option to generate additional output for integration with TeamCity. If you don't need this output remove that option.

### Run Functional Tests ###

Call `./vendor/bin/phpunit --teamcity tests` command from `local_ignite_path/modules/platforms/php` folder.

### Run Examples Executors ###

Call `./vendor/bin/phpunit --teamcity tests/examples/ExecuteExamples.php` command from `local_ignite_path/modules/platforms/php` folder.

### Run AuthTlsExample Executor ###

It requires running Apache Ignite server with non-default configuration (authentication and TLS switched on).

If the server runs locally:
- setup the server to accept TLS. During the setup use `keystore.jks` and `truststore.jks` certificates from `local_ignite_path/modules/platforms/php/examples/certs/` folder. Password for the files: `123456`
- switch on the authentication on the server. Use the default username/password.

If the server runs remotely, and/or other certificates are required, and/or non-default username/password is required - see this [instruction](#additional-setup-for-authtlsexample).

Call `./vendor/bin/phpunit --teamcity tests/examples/ExecuteAuthTlsExample.php` command from `local_ignite_path/modules/platforms/php` folder.

---------------------------------------------------------------------

# API spec generation: instruction #

It must be done if a public API class/method has been changed.
1. Install Doxygen (http://doxygen.org/download.html)
2. Clone or download Ignite repository https://github.com/apache/ignite.git to `local_ignite_path`
3. Go to `local_ignite_path/modules/platforms/php`
4. Execute `doxygen api_docs/Doxyfile` command. The generated documentation is placed in `local_ignite_path/modules/platforms/php/api_docs/html` folder.

Note: `local_ignite_path/modules/platforms/php/api_docs/Doxyfile` is a file with Doxygen configuration.

---------------------------------------------------------------------

# Release the client in the PHP Package Repository: instruction #

1. Register an account at Packagist (https://packagist.org/), if not registered yet

2. Prepare/update composer.json file. 

Example of this file is [here](./composer.json). 

Pay attention to:
   - "name" - name of the package
   - "description" - description of the package
   - "keywords" - keywords for the search of the package on Packagist
   - "license", "homepage", "authors"
   - other properties depend on the implementation/tests, do not touch them

Note: The current version of Packagist requires composer.json file must be in the root of a repository.
(https://github.com/composer/packagist/issues/472)

3. Create git tag with a new version name.
Packagist obtains package versions from git tags. Tag names should match 'X.Y.Z' or 'vX.Y.Z' pattern, with an optional suffix.

4. Publish/update the package.

To publish the package the first time 
- Go to https://packagist.org/packages/submit
- Enter the client Repository URL and click "Check", click "Submit"

To update the existing package
- Go to https://packagist.org/packages/apache/apache-ignite-client (assuming `apache/apache-ignite-client` is the name of the package) and click "Update"
