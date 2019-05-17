/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

const Util = require('util');
const Errors = require('../Errors');
const IgniteClient = require('../IgniteClient');
const ClientSocket = require('./ClientSocket');
const ArgumentChecker = require('./ArgumentChecker');
const Logger = require('./Logger');

class Router {

    constructor(onStateChanged) {
        this._state = IgniteClient.STATE.DISCONNECTED;
        this._onStateChanged = onStateChanged;

        // Affinity Awareness disabled by default
        // Declare variables for the case with one active connection
        this._socket = null;
    }

    async connect(communicator, config) {
        this._communicator = communicator;

        if (this._state !== IgniteClient.STATE.DISCONNECTED) {
            throw new Errors.IllegalStateError();
        }

        this._config = config;
        await this._connect();
    }

    disconnect() {
        if (this._state !== IgniteClient.STATE.DISCONNECTED) {
            this._changeState(IgniteClient.STATE.DISCONNECTED);

            if (!this._affinityAwareness && this._socket) {
                this._socket.disconnect();
                this._socket = null;
            }
            else if (this._affinityAwareness) {
                for (let uuid in this._connections) {
                    const socket = this._connections[uuid];
                    socket.disconnect();
                }
                this._connections = {};
            }
        }
    }

    async send(opCode, payloadWriter, payloadReader = null, affinityHint = null) {
        if (this._state !== IgniteClient.STATE.CONNECTED) {
            throw new Errors.IllegalStateError();
        }

        if (!this._affinityAwareness) {
            await this._socket.sendRequest(opCode, payloadWriter, payloadReader);
        }
        else {
            const bestConnection = await this._chooseConnection(affinityHint);
            // console.log("Endpoint chosen: " + bestConnection.endpoint);
            await bestConnection.sendRequest(opCode, payloadWriter, payloadReader);
        }

    }

    async _connect() {
        this._turnOffAffinityAwareness();
        await this._connectFailover();

        if (this._socket.nodeUUID !== undefined) {
            const connectedEndpoint = this._socket.endpoint;
            this._turnOnAffinityAwareness();
            this._deadEndpoints = this._config._endpoints.filter((endpoint) => endpoint !== connectedEndpoint);
            this._probeEndpoints();
        }
    }

    async _connectFailover() {
        const errors = new Array();
        let endpoint;
        const endpoints = this._config._endpoints;

        // TODO: Randomize?
        for (let i = 0; i < endpoints.length; i++) {
            endpoint = endpoints[i];
            try {
                this._changeState(IgniteClient.STATE.CONNECTING, endpoint);
                this._socket = new ClientSocket(
                    endpoint, this._config, this._communicator, this._onSocketDisconnect.bind(this));
                await this._socket.connect();
                this._changeState(IgniteClient.STATE.CONNECTED, endpoint);
                return;
            }
            catch (err) {
                errors.push(Util.format('[%s] %s', endpoint, err.message));
            }
        }
        const error = errors.join('; ');
        this._changeState(IgniteClient.STATE.DISCONNECTED, endpoint, error);
        this._socket = null;
        throw new Errors.IgniteClientError(error);
    }

    async _onSocketDisconnect(socket, error = null) {
        if (this._affinityAwareness) {
            delete this._connections[socket.nodeUUID];
            if (Object.keys(this._connections).length != 0) {
                // TODO: Try to reconnect?
                return;
            }
        }

        await this._connect();
    }

    _changeState(state, endpoint = null, reason = null) {
        if (Logger.debug) {
            Logger.logDebug(Util.format('Socket %s: %s -> %s'),
                endpoint ? endpoint : this._socket ? this._socket._endpoint : '',
                this._getState(this._state),
                this._getState(state));
        }
        if (this._state !== state) {
            this._state = state;
            if (this._onStateChanged) {
                this._onStateChanged(state, reason);
            }
        }
    }

    _getState(state) {
        switch (state) {
            case IgniteClient.STATE.DISCONNECTED:
                return 'DISCONNECTED';
            case IgniteClient.STATE.CONNECTING:
                return 'CONNECTING';
            case IgniteClient.STATE.CONNECTED:
                return 'CONNECTED';
            default:
                return 'UNKNOWN';
        }
    }

    /** Affinity Awareness methods */

    async _chooseConnection(affinityHint) {
        // TODO: Implement the Best Effort Affinity algo here

        const connectionsNum = Object.keys(this._connections).length;
        return Object.values(this._connections)[Math.floor(Math.random() * connectionsNum)];
    }

    async _probeEndpoints() {
        for (let i in this._deadEndpoints) {
            const endpoint = this._deadEndpoints[i];
            try {
                const socket = new ClientSocket(
                    endpoint, this._config, this._communicator, this._onSocketDisconnect.bind(this));
                await socket.connect();
                this._addNode(socket);
            }
            catch (err) {
            }
        }
    }

    _turnOnAffinityAwareness() {
        this._affinityAwareness = true;
        // Node UUID -> [endpoint1, endpoint2, ...]
        this._nodes = {};
        // Endpoints which we never connected to
        this._deadEndpoints = [];
        // Node UUID -> ClientSocket instance
        this._connections = {};

        // Fill the Affinity Awareness data structures and remove the _socket field as we don't need it anymore
        this._addNode(this._socket);
        delete this._socket;
    }

    _turnOffAffinityAwareness() {
        if (!this._affinityAwareness) {
            return;
        }

        delete this._nodes;
        delete this._deadEndpoints;
        delete this._connections;
        delete this._affinityAwareness;
    }

    _addNode(socket) {
        const nodeUUID = socket.nodeUUID;
        const endpoint = socket.endpoint;

        if (nodeUUID in this._nodes) {
            // This can happen if the same node has several IPs
            this._nodes[nodeUUID].push(endpoint);
            // We will keep more fresh connection alive
            this._connections[nodeUUID].disconnect();
        }
        else {
            this._nodes[nodeUUID] = [endpoint];
        }

        this._connections[nodeUUID] = socket;
    }
}

module.exports = Router;
