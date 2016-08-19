"use strict";
var request = require('request');

function DeviceConfig(erouter, subscription, config, log) {
    this.knownDevices = {};
    var self = this;

    this.query_all_devices_info = function() {
        var url = config['ACCOUNT_MANAGEMENT_SERVICE'] + '/device';
        request.get(url, function(err, response) {
            if (err) {
                log.error({
                    err: err
                }, "Error response from all devices config request");
            } else {
                var data = JSON.parse(response.body);
                if (data['err']) {
                    log.error('Query for all devices info failed. Error: %s', data['err']);
                } else {
                    this.knownDevices = {};
                    for (var i = 0; i < data['result'].length; i++) {
                        if (data['result'][i]['active'] === true) {
                            self.knownDevices[data['result'][i]['deviceid']] = {};
                            self.knownDevices[data['result'][i]['deviceid']]['key'] = data['result'][i]['key'];
                            self.knownDevices[data['result'][i]['deviceid']]['stats_active'] = data['result'][i]['stats_active'];
                            log.info('Update device %s with key %s in device config cache.', data['result'][i]['deviceid'], data['result'][i]['key']);
                        }
                    }
                }
            }
        });
    };

    this.query_device_info = function(deviceid) {
        var url = config['ACCOUNT_MANAGEMENT_SERVICE'] + '/device/' + deviceid;
        request.get(url, function(err, response) {
            if (err) {
                log.error({
                        err: err
                    },
                    "Error response from device config request."
                );
            } else {
                try {
                    var data = JSON.parse(response.body);
                    if (data['err']) {
                        log.error('Query for device info failed. Error: %s', data['err']);
                    } else if (data['result']['active'] === true) {
                        if (self.knownDevices[data['result']['deviceid']] === undefined) {
                            self.knownDevices[data['result']['deviceid']] = {};
                        }
                        self.knownDevices[data['result']['deviceid']]['key'] = data['result']['key'];
                        self.knownDevices[data['result']['deviceid']]['stats_active'] = data['result']['stats_active'];
                        log.info('Update device %s with key %s in device config cache.', data['result']['deviceid'], data['result']['key']);
                    } else {
                        log.info('Remove inactive device %s from device config cache.', data['result']['deviceid']);
                        delete self.knownDevices[data['result']['deviceid']];
                    }
                } catch (err) {
                    log.error({
                        err: err
                    }, 'Can not process device query event.');
                }
            }
        });
    };

    erouter.subscribe('device_config_update', subscription, function(err, data) {
        if (err) {
            log.error({
                err: err
            }, "Error at device_config_update device_config_update.");
        } else if (data) {
            try {
                var device = JSON.parse(data);
                self.query_device_info(device['deviceid']);
                log.info("%s received new config for device %s", subscription, device['deviceid']);
            } catch (err) {
                log.error({
                    err: err
                }, 'Can not process device update event.');
            }
        }
    });

}

DeviceConfig.prototype.validateDevice = function(deviceid, key) {
    if (this.knownDevices[deviceid] !== undefined) {
        return this.knownDevices[deviceid]['key'] === key;
    }
    return false;
};

DeviceConfig.prototype.active = function(deviceid) {
    if (this.knownDevices[deviceid] !== undefined) {
        return this.knownDevices[deviceid]['active'];
    }
    return false;
};

DeviceConfig.prototype.stats_active = function(deviceid) {
    if (this.knownDevices[deviceid] !== undefined) {
        return this.knownDevices[deviceid]['stats_active'];
    }
    return false;
};
module.exports = DeviceConfig;
