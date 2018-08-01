# PHP Thin Client #

## Overview ##

This thin client allows your PHP applications to work with Apache Ignite clusters via [Binary Client Protocol](https://apacheignite.readme.io/v2.6/docs/binary-client-protocol).

A thin client is a lightweight Ignite client that connects to the cluster via a standard socket connection. It does not start in JVM process (Java is not required at all), does not become a part of the cluster topology, never holds any data or used as a destination of compute grid calculations.

What it does is it simply establishes a socket connection to a standard Ignite node and performs all operations through that node.

## Installation ##

PHP version 7.2 or higher is required.
??? (download and install)

### Installation from the PHP Package Repository ###

TODO

### Installation from Sources ###

???

## Quick Start ##

TODO

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

TODO

## Usage ##

TODO

## Examples ##

TODO

## Tests ##

TODO

