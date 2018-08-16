# PHP Thin Client #

## Overview ##

This thin client allows your PHP applications to work with Apache Ignite clusters via [Binary Client Protocol](https://apacheignite.readme.io/v2.6/docs/binary-client-protocol).

A thin client is a lightweight Ignite client that connects to the cluster via a standard socket connection. It does not start in JVM process (Java is not required at all), does not become a part of the cluster topology, never holds any data or used as a destination of compute grid calculations.

What it does is it simply establishes a socket connection to a standard Ignite node and performs all operations through that node.

## Installation ##

PHP version 7.2 or higher is required.
TODO (download and install)

### Installation from the PHP Package Repository ###

TODO

### Installation from Sources ###

TODO

## Quick Start ##

Let's use existing [PHP examples]([./examples]) that are delivered with every Ignite distribution for the sake of quick getting started.

Before connecting to Ignite from PHP thin client, start at least one Ignite cluster node. For instance, you can use `ignite.sh` script as follows:

In Unix:
```bash
./ignite.sh
```

In Windows:
```bash
ignite.bat
```

Link Ignite PHP examples if you haven't done this yet: TODO

If needed, modify ENDPOINT constant in an example source file which represents a remote Ignite node endpoint. The default value is 127.0.0.1:10800.

Run an example by calling `TODO`, as follows: TODO

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

An application can specify an Ignite type of a field by an instance of the [ComplexObjectType](TODO:link) class which references a PHP class. In this case, when the application reads a value of the field, the client deserializes the received Ignite Complex Object and returns it to the client as an instance of the referenced PHP class. When the application writes a value of the field, the client expects an instance of the referenced PHP class and serializes it to the Ignite Complex Object.

If an application does not specify an Ignite type of a field and reads a value of the field, the client returns the received Ignite Complex Object as an instance of the [BinaryObject](TODO:link) class - a binary form of the Ignite Complex Object. The `BinaryObject` allows working with its content (read and write values of the object's fields, add and remove the fields, etc.) avoiding deserialization. Also, the application can create an instance of the `BinaryObject` class from a PHP object. An application can write the `BinaryObject` as a value of a field into Ignite, if that field has no explicitly specified Ignite type.

The client takes care of obtaining or registering information about Ignite Complex Object type, including schema, from/at Ignite cluster. It is done automatically by the client, when required for reading or writing of the Ignite Complex Object from/to Ignite.

## Usage ##

The below sections explain the basic steps to work with Apache Ignite using PHP client.

### Prerequisites ###

Before connecting to Ignite from PHP thin client, start at least one Ignite cluster node. For instance, you can use `ignite.sh` script as follows:

In Unix:
```bash
./ignite.sh
```

In Windows:
```bash
ignite.bat
```

### Instantiating Ignite Client ###

A usage of the client starts with the creation of a [Client](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_client.html) object that connects a PHP application to the cluster.

It is possible to create as many `Client` objects as needed. All of them will work independently.

TODO: example

### Configuring Ignite Client ###

The next step is to define a configuration for the client's connection by populating [ClientConfiguration](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/class_apache_1_1_ignite_1_1_client_configuration.html) object.

A mandatory part of the configuration, which is specified in the constructor, is a list of endpoints of the Ignite nodes. At least one endpoint must be specified. A client connects to one node only - a random endpoint from the provided list. Other nodes, if provided, are used by the client for the "failover re-connection algorithm": the client tries to re-connect to the next random endpoint from the list if the current connection is lost.

Optional parts of the configuration can be specified using additional methods which include: TODO
- Authentication using username/password.
- SSL/TLS connection.
- PHP connection options.

By default, the client establishes a non-secure connection with default connection options defined by PHP and does not use authentication.

The example below shows how to configure the client:

TODO: example

The next example shows how to prepare Ignite Client Configuration with username/password authentication and additional connection options:

TODO: example

### Connecting to the Cluster ###

The next step is to connect the client to an Ignite cluster. The configuration for the client's connection, which includes endpoint(s) to connect to, is specified in the connect method.

If the client is not connected (including the case it can not successfully reconnect using the "failover re-connection algorithm"), the [TODO:Exception](TODO:link) is thrown for any operation with a cache.

If the client unexpectedly losts the connection during an operation, the [TODO:Exception](TODO:link) is thrown. In this case, it is not known if the operation has been actually executed in the cluster or not.

At any moment, an application can forcibly disconnect the client by calling the disconnect method.

When the client becomes disconnected, an application can call the connect method again - with the same or different configuration (eg. with a different list of endpoints).

TODO: example

### Caches Usage and Configuration ###

The next step is to obtain an object representing an Ignite cache. It's an instance of a PHP class with the [CacheInterface](https://rawgit.com/nobitlost/ignite/ignite-7783-docs/modules/platforms/php/api_docs/html/interface_apache_1_1_ignite_1_1_cache_interface.html).

The thin client provides several methods to work with Ignite caches and to obtain objects with the `CacheInterface` - get a cache by its name, create a cache with a specified name and optional cache configuration, get or create a cache, destroys a cache, etc.

It is possible to obtain as many objects with the `CacheInterface` as needed - for the same or different Ignite caches - and work with all of them in parallel.

The following example shows how to get access to a cache by name and destroy its later:

TODO: example

The next example shows how to get access to a cache by name and with a configuration:

TODO: example

This example shows how to get an existing cache by name:

TODO: example

### Types Mapping Configuration ###

The next step is optional.

It is possible to specify concrete Ignite types for the key and/or the value of the cache. If the key and/or value is a non-primitive type (eg. a map, a collection, a complex object, etc.) it is possible to specify concrete Ignite types for fields of that objects as well.

If Ignite type is not explicitly specified for some field, the client tries to make automatic default mapping between PHP types and Ignite object types.

More details about types and mappings are clarified in the [Data Types](#data-types) section.

TODO: example

At this point, we're ready to start working with the data stored or to be placed in Ignite.

### Key-Value Queries ###

The `CacheInterface` provides methods to work with the key and the value of the cache using Key-Value operations - put, get, put all, get all, replace and others. This example shows how to do that:

TODO: example

Now, let's see how to put/get Complex Objects and Binary Objects:

TODO: example

### SQL and Scan Queries ###

PHP client supports Ignite SQL and scan queries. A query method returns a cursor object with the standard PHP Iterator interface which allows to iterate over the set with the query results lazily, one by one. Additionally, the cursor has methods to get the whole results at once.

#### Scan Query ####

First, define the query by creating and configuring an instance of the [ScanQuery](TODO:link) class.

Then, pass the `ScanQuery` instance to the query method of the `CacheInterface`.

Finally, use the returned object with the [CursorInterface](TODO:link) to iterate over or get all cache entries returned by the query.

TODO: example

#### SQL Query ####

First, define the query by creating and configuring an instance of the [SqlQuery](TODO:link) class.

Then, pass the `SqlQuery` instance to the query method of the `CacheInterface`.

Finally, use the returned object with the [CursorInterface](TODO:link) to iterate over or get all cache entries returned by the query.

TODO: example

#### SQL Fields Query ####

This type of queries is used to obtain individual fields as a part of an SQL query result set, execute DML and DDL statements such as INSERT, UPDATE, DELETE, CREATE and other.

First, define the query by creating and configuring an instance of the [SqlFieldsQuery](TODO:link) class.

Then, pass the `SqlFieldsQuery` instance to the query method of the `CacheInterface`.

Finally, use the returned object with the [SqlFieldsCursorInterface](TODO:link) to iterate over or get all elements returned by the query.

TODO: example

### Enabling Debug ###

To switch on/off the client's debug output (including errors logging), call `setDebug()` method of the Ignite `Client` object. Debug output is disabled by default.

TODO: example

## Full Examples ##

PHP Thin Client contains fully workable examples to demonstrate the main behavior of the client.

### Examples Description ###

TODO: check and update

#### Sql Example ####

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

#### Cache Put Get Example ####

Source: [CachePutGetExample.php](./examples/CachePutGetExample.php)

This example demonstrates basic Cache, Key-Value Queries and Scan Query operations:
- connects to a node
- creates a cache, if it doesn't exist
  - specifies key type as Integer
- executes different cache operations with Complex Objects and Binary Objects
  - put several objects in parallel
  - putAll
  - get
  - getAll
  - ScanQuery
- destroys the cache

#### Sql Query Entries Example ####

Source: [SqlQueryEntriesExample.php](./examples/SqlQueryEntriesExample.php)

This example demonstrates basic Cache, Key-Value Queries and SQL Query operations:
- connects to a node
- creates a cache from CacheConfiguration, if it doesn't exist
- writes data of primitive and Complex Object types into the cache using Key-Value put operation
- reads data from the cache using SQL Query
- destroys the cache

#### Auth Tls Example ####

Source: [AuthTlsExample.php](./examples/AuthTlsExample.php)

This example requires [additional setup](#additional-setup-for-authtlsexample).

This example demonstrates how to establish a secure connection to an Ignite node and use username/password authentication, as well as basic Key-Value Queries operations for primitive types:
- connects to a node using TLS and providing username/password
- creates a cache, if it doesn't exist
  - specifies key and value type of the cache
- put data of primitive types into the cache
- get data from the cache
- destroys the cache

### Examples Installation ###

TODO

### Examples Setup and Running ###

TODO: check and update

1. Run Apache Ignite server - locally or remotely.

2. If needed, modify `ENDPOINT` constant in an example source file - Ignite node endpoint. The default value is `127.0.0.1:10800`.

3. Run an example by TODO

### Additional Setup for AuthTlsExample ###

TODO: check and update

1. Obtain certificates required for TLS:
  - either use pre-generated certificates provided in the [examples/certs](./certs) folder. Password for the files: `123456`. Note, these certificates work for an Ignite server installed locally only.
  - or obtain other existing certificates applicable for a concrete Ignite server.
  - or generate new certificates applicable for a concrete Ignite server.

  - The following files are needed:
    - keystore.jks, truststore.jks - for the server side
    - client.key, client.crt, ca.crt - for the client side

2. Place client.key, client.crt and ca.crt files somewhere locally, eg. into the [examples/certs](.examples/certs) folder.

3. If needed, modify `TLS_KEY_FILE_NAME`, `TLS_CERT_FILE_NAME` and `TLS_CA_FILE_NAME` constants in the example source file. The default values point to the files in the [examples/certs](.example/certs) folder.

4. Setup Apache Ignite server to accept TLS - see appropriate Ignite documentation. Provide the obtained keystore.jks and truststore.jks certificates during the setup.

5. Switch on and setup authentication in Apache Ignite server - see appropriate Ignite documentation.

6. If needed, modify `USER_NAME` and `PASSWORD` constants in the example source file. The default values are the default Ignite username/password.

7. Executes [Setup and Running](#examples-setup-and-running) steps.

## Tests ##

TODO

## API spec generation: instruction ##

TODO

## Release the client in the PHP Package Repository: instruction ##

TODO
