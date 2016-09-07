import json
import logging
from lwutils.accountmanagementservice_client import AccountManagementPersistenceService
from lwutils.erouter_client import ERouterClient


class DeviceConfigHandler():

    def __init__(self, config, applicaction_name, devices={}, engage=True):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.devices = devices
        self.erouter_client = ERouterClient(self.config.get("EROUTER_SERVICE_URL"))
        self.application_name = applicaction_name
        if engage:
            self.engage()

    def engage(self):
        try:
            self.erouter_client.subscribe("device_config_update", self.application_name, self.update_device_config_callback)
            self.logger.info('Subscribe %s to device config updates', self.application_name)
        except:
            self.logger.exception("An error occurred while initing the event bus from %s.", (self.application_name))
        self.update_all_devices()

    def update_device_config_callback(self, data):
        if data:
            msg = json.loads(data)
            if 'deviceid' in msg:
                device = AccountManagementPersistenceService.get_device(self.config["ACCOUNT_MANAGEMENT_SERVICE"], msg['deviceid'])
                self.devices[msg['deviceid']] = device.to_dict()
                self.logger.info('%s received new config for device %s' % (self.application_name, msg['deviceid']))

    def update_all_devices(self):
        self.logger.info('Update all devices for %s' % self.application_name)
        devices = AccountManagementPersistenceService.get_all_devices(self.config["ACCOUNT_MANAGEMENT_SERVICE"])
        for device in devices:
            self.devices[device.deviceid] = device.to_dict()
            self.logger.info('%s received new config for device %s' % (self.application_name, device.deviceid))
