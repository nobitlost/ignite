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

import socket
import ssl

from pyignite.constants import *
from pyignite.exceptions import ParameterError, SocketError, SocketWriteError
from .handshake import HandshakeRequest, read_response


class Connection:
    """
    Socket wrapper. Detects fragmentation and network errors.

    https://docs.python.org/3/howto/sockets.html
    """

    socket = None
    host = None
    port = None

    @staticmethod
    def check_kwargs(kwargs):
        expected_args = [
            'use_ssl',
            'ssl_version',
            'ssl_ciphers',
            'ssl_cert_requires',
            'ssl_keyfile',
            'ssl_certfile',
        ]
        for kw in kwargs:
            if kw not in expected_args:
                raise ParameterError((
                    'Unexpected parameter for connection '
                    'initialization: `{}`'
                ).format(kw))

    def __init__(self, **kwargs):
        """
        Initialize connection.

        For the use of the last two parameters see
        https://docs.python.org/3/library/ssl.html#ssl-certificates.

        :param use_ssl: (optional) set to True if Ignite server uses SSL
         on its binary connector. Defaults to not use SSL,
        :param ssl_version: (optional) SSL version constant from standard
         `ssl` module. Defaults to TLS v1.1, as in Ignite 2.5,
        :param ssl_ciphers: (optional) ciphers to use. If not provided,
         `ssl` default ciphers are used,
        :param ssl_cert_requires: (optional) determines how the remote side
         certificate is treated:
         * `ssl.CERT_NONE` − remote certificate is ignored (default),
         * `ssl.CERT_OPTIONAL` − remote certificate will be validated,
           if provided,
         * `ssl.CERT_REQUIRED` − valid remote certificate is required,
        :param ssl_keyfile: (optional) a path to SSL key file to identify
         local party,
        :param ssl_certfile: (optional) a path to ssl certificate file
         to identify local party.
        """
        self.check_kwargs(kwargs)
        self.init_kwargs = kwargs

        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if getattr(kwargs, 'use_ssl', None):
            _socket = ssl.wrap_socket(
                _socket,
                ssl_version=getattr(kwargs, 'ssl_version', SSL_DEFAULT_VERSION),
                ciphers=getattr(kwargs, 'ssl_ciphers', SSL_DEFAULT_CIPHERS),
                cert_reqs=getattr(kwargs, 'ssl_cert_requires', ssl.CERT_NONE),
                keyfile=getattr(kwargs, 'ssl_keyfile', None),
                certfile=getattr(kwargs, 'ssl_certfile', None),
            )
        self.socket = _socket

    read_response = read_response

    def connect(self, host: str, port: int):
        """
        Connect to the server.

        :param host: Ignite server host,
        :param port: Ignite server port.
        """
        if self.socket is not None:
            self.socket.connect((host, port))

        hs_request = HandshakeRequest()
        self.send(hs_request)
        hs_response = self.read_response()
        if hs_response.op_code == 0:
            self.close()
            raise SocketError(
                (
                    'Ignite protocol version mismatch: requested {}.{}.{}, '
                    'received {}.{}.{}.'
                ).format(
                    PROTOCOL_VERSION_MAJOR,
                    PROTOCOL_VERSION_MINOR,
                    PROTOCOL_VERSION_PATCH,
                    hs_response.version_major,
                    hs_response.version_minor,
                    hs_response.version_patch,
                )
            )
        self.host, self.port = host, port

    def clone(self) -> object:
        clone = Connection(**self.init_kwargs)
        if self.port and self.host:
            clone.connect(self.host, self.port)
        return clone

    def make_buffered(self, buffer: bytes) -> object:
        conn = BufferedConnection(buffer, **self.init_kwargs)
        if self.port and self.host:
            conn.connect(self.host, self.port)
        return conn

    def send(self, data: bytes, flags=None):
        """
        Send data down the socket.

        :param data: bytes to send,
        :param flags: (optional) OS-specific flags.
        """
        kwargs = {}
        if flags is not None:
            kwargs['flags'] = flags
        data = bytes(data)
        total_bytes_sent = 0

        while total_bytes_sent < len(data):
            bytes_sent = self.socket.send(data[total_bytes_sent:], **kwargs)
            if bytes_sent == 0:
                self.socket.close()
                raise SocketError('Socket connection broken.')
            total_bytes_sent += bytes_sent

    def recv(self, buffersize, flags=None) -> bytes:
        """
        Receive data from socket.

        :param buffersize: bytes to receive,
        :param flags: (optional) OS-specific flags,
        :return: data received.
        """
        kwargs = {}
        if flags is not None:
            kwargs['flags'] = flags
        chunks = []
        bytes_rcvd = 0

        while bytes_rcvd < buffersize:
            chunk = self.socket.recv(buffersize-bytes_rcvd, **kwargs)
            if chunk == b'':
                self.socket.close()
                raise SocketError('Socket connection broken.')
            chunks.append(chunk)
            bytes_rcvd += len(chunk)

        return b''.join(chunks)

    def close(self):
        """
        Mark socket closed. This is recommended but not required, since
        sockets are automatically closed when they are garbage-collected.
        """
        self.socket.close()
        self.host = self.port = None


class BufferedConnection(Connection):
    """
    Mock socket reads. Allows deserializers to work with static buffers.

    You most probably do not need to use this class directly.
    Call `Connection.make_buffered()` instead.
    """

    def __init__(self, buffer: bytes, **kwargs):
        self.buffer = buffer
        self.init_kwargs = kwargs
        self.pos = 0

    def connect(self, host: str, port: int):
        self.host, self.port = host, port

    def close(self):
        self.host = self.port = None

    def send(self, data: bytes):
        raise SocketWriteError(
            'Attempt to send `{}` to read-only connection'.format(data)
        )

    def recv(self, buffersize: int):
        received = self.buffer[self.pos:self.pos+buffersize]
        self.pos += buffersize
        return received


class PrefetchConnection(Connection):
    """
    Use this socket wrapper, when you wish to “put back” some data you just
    receive from the socket.
    """
    prefetch = None
    conn = None

    def __init__(self, conn: Connection, prefetch: bytes=b''):
        super().__init__()
        self.conn = conn
        self.prefetch = prefetch

    def recv(self, buffersize, flags=None):
        pref_size = len(self.prefetch)
        if buffersize > pref_size:
            result = self.prefetch + self.conn.recv(
                buffersize-pref_size, flags)
            self.prefetch = b''
            return result
        else:
            result = self.prefetch[:buffersize]
            self.prefetch = self.prefetch[buffersize:]
            return result
