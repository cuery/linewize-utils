/*jshint expr: true*/
/*jshint unused: false*/

"use strict";
var DeviceConfig = require('../deviceConfig');
var assert = require('chai').assert;
var should = require('chai').should();
var config = require('config').config;
var http = require('http');

describe('Device config', function() {
    var eventbus = {};
    var log = {};

    var deviceConfigResponse = {
        "result": {
            "description": null,
            "deviceid": "myDevice",
            "edgewize": false,
            "key": "mySecureKey",
            "last_status": false,
            "last_version": null,
            "monitored": true,
            "notifiables": [],
            "report_emails": "",
            "routed_network": true,
            "surfwize": true,
            "active": true,
            "stats_active": true,
            "timezone": "Europe/Berlin",
            "user_defined_name": "TCDevice"
        }
    };

    log.info = function(msg) {};
    log.error = function(msg) {};

    eventbus.publish = function(event, msg, callback) {
        var data = {};
        data.event = event;
        data.msg = msg;
        eventbus.publish.published.push(data);
        callback(null, 'xxx');
    };

    eventbus.subscribe = function(event, subscription, callback) {
        eventbus.sub.event = event;
        eventbus.sub.subscription = subscription;
        eventbus.sub.callback = callback;
    };

    eventbus.Events = {
        'SCLOUD_MANAGER_ACTIVE': 'scloud_manager_active',
        'SCLOUD_MAINTENANCE_ACTIVE': 'scloud_maintenance_active'
    };

    beforeEach(function() {
        eventbus.publish.published = [];
        eventbus.sub = {};
        eventbus.sub.event = null;
        eventbus.sub.subscription = null;
    });

    it('should subscribe to devcie_config_update event', function(done) {
        var deviceConfig = new DeviceConfig(eventbus, 'devUpd__scloud_manager', {}, log);
        assert.equal('device_config_update', eventbus.sub.event);
        assert.ok(eventbus.sub.subscription.indexOf('devUpd__scloud_manager') > -1);
        done();
    });

    it('should update query device info for a device_config_update event', function(done) {
        var deviceInfoQueried = false;
        var config = {
            "ACCOUNT_MANAGEMENT_SERVICE": "http://localhost:5008"
        };
        var expectedKnownDevices = {
            "myDevice": {
                "key": "mySecureKey",
                "stats_active": true
            }
        };

        var server = http.createServer(function(req, res) {
            deviceInfoQueried = true;
            res.writeHead(200);
            res.end(JSON.stringify(deviceConfigResponse));
        });
        server.listen(5008);

        var deviceConfig = new DeviceConfig(eventbus, 'scloud_manager', config, log);
        var device = {
            deviceid: "myDevice"
        };
        eventbus.sub.callback(null, JSON.stringify(device));

        setTimeout(function() {
            assert.ok(deviceInfoQueried);
            assert.equal(JSON.stringify(expectedKnownDevices), JSON.stringify(deviceConfig.knownDevices));
            server.close();
            done();
        }, 50);

    });

    it('should delete query device info for a device_config_update event with inactive device', function(done) {
        var deviceInfoQueried = false;
        var config = {
            "ACCOUNT_MANAGEMENT_SERVICE": "http://localhost:5008"
        };

        var inactiveDeviceConfigResponse = {
            "result": {
                "description": null,
                "deviceid": "myDevice",
                "edgewize": false,
                "key": "mySecureKey",
                "last_status": false,
                "last_version": null,
                "monitored": true,
                "notifiables": [],
                "report_emails": "",
                "routed_network": true,
                "surfwize": true,
                "active": false,
                "stats_active": false,
                "timezone": "Europe/Berlin",
                "user_defined_name": "TCDevice"
            }
        };

        var server = http.createServer(function(req, res) {
            deviceInfoQueried = true;
            res.writeHead(200);
            res.end(JSON.stringify(inactiveDeviceConfigResponse));
        });
        server.listen(5008);

        var deviceConfig = new DeviceConfig(eventbus, 'scloud_manager', config, log);
        var device = {
            deviceid: "myDevice"
        };
        eventbus.sub.callback(null, JSON.stringify(device));

        setTimeout(function() {
            assert.ok(deviceInfoQueried);
            assert.equal(JSON.stringify({}), JSON.stringify(deviceConfig.knownDevices));
            server.close();
            done();
        }, 50);

    });

    it('should validate given deviceid and key', function(done) {
        var deviceConfig = new DeviceConfig(eventbus, 'scloud_manager', {}, log);
        deviceConfig.knownDevices['myDevice'] = {};
        deviceConfig.knownDevices['myDevice']['key'] = 'myKey';
        assert.ok(deviceConfig.validateDevice('myDevice', 'myKey'));
        assert.notOk(deviceConfig.validateDevice('myDevice', 'myWrongKey'));
        assert.notOk(deviceConfig.validateDevice('myUnknownDevice', 'myKey'));
        done();
    });
});