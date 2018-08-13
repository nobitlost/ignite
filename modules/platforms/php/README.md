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

TODO

The client provides two ways to operate with Ignite Complex Object type - in the deserialized form and the binary form.

An application can specify an Ignite type of a field by an instance of the `ComplexObjectType` class which references an instance of a PHP object. In this case, when the application reads a value of the field, the client deserializes the received Ignite Complex Object and returns it to the client as an instance of the corresponding JavaScript Object. When the application writes a value of the field, the client expects an instance of the corresponding JavaScript Object and serializes it to the Ignite Complex Object.

If an application does not specify an Ignite type of a field and reads a value of the field, the client returns the received Ignite Complex Object as an instance of the [`BinaryObject`](doc:binary-marshaller) class - a binary form of the Ignite Complex Object. The `BinaryObject` allows working with its content avoiding deserialization (read and write values of the object's fields, add and remove the fields, etc.) Also, the application can create an instance of the `BinaryObject` class from a JavaScript Object. An application can write the `BinaryObject` as a value of a field into Ignite, if that field has no explicitly specified Ignite type.

The client takes care of obtaining or registering information about Ignite Complex Object type, including schema, from/at Ignite cluster. It is done automatically by the client, when required for reading or writing of the Ignite Complex Object from/to Ignite.

## Usage ##

TODO

## Examples ##

TODO

## Tests ##

TODO

