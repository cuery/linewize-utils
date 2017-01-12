import json
import unittest
import httpretty
from lwutils.device_config_handler import DeviceConfigHandler


class DeviceHandlerTestCase(unittest.TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    @httpretty.activate
    def test_callback(self):
        config = {
            "ACCOUNT_MANAGEMENT_SERVICE": "http://service",
            "EROUTER_SERVICE_URL": "http://erouterurl"
        }

        handler = DeviceConfigHandler(config, 'my_app', engage=False)

        device = {
            "key": "null",
            "last_version": "null",
            "labels": [],
            "hardware": "null",
            "report_emails": "null",
            "invoice_number": 0,
            "edgewize": False,
            "timezone": "null",
            "beta_tester": False,
            "classroom_groups": [],
            "monitored": True,
            "education_institute_number": 0,
            "stats_active": True,
            "white_label_file_name": "null",
            "routed_network": True,
            "deal_url": "null",
            "description": "",
            "allow_public_source_ip": False,
            "classroom_exceptions": [],
            "user_defined_name": "null",
            "active": True,
            "mylinewize_login": "null",
            "paid_subscription": False,
            "reseller": "null",
            "install_date": "null",
            "classroom_allow_owner_access": False,
            "failover_active": False,
            "customer_type": "null",
            "deviceid": "testdevice1",
            "surfwize": False,
            "inventory": None,
            "update_allow_auto": True,
            "update_branch": "stable",
            "classroom_groups_group_prefix": None,
            "classroom_restrict_global_teachers": False,
            "classwize_reliever_enabled": False,
            "xero_id": "null",
            "msp": "null",
            "watchdog_recipients": []
        }
        httpretty.register_uri(
            httpretty.GET, uri="http://service/device/testdevice1", body=json.dumps(dict(result=device)))

        handler.update_device_config_callback(json.dumps({"deviceid": "testdevice1"}))
        print json.dumps(device)
        print json.dumps(handler.devices.get("testdevice1"))
        assert handler.devices.get("testdevice1") == device

    @httpretty.activate
    def test_update_all_devices(self):
        self.maxDiff = None

        config = {
            "ACCOUNT_MANAGEMENT_SERVICE": "http://accountmanagementserviceurl",
            "EROUTER_SERVICE_URL": "http://erouterurl"
        }

        device1 = {
            "key": "null",
            "last_version": "null",
            "labels": [],
            "hardware": "null",
            "report_emails": "null",
            "invoice_number": 0,
            "edgewize": False,
            "timezone": "null",
            "beta_tester": False,
            "classroom_groups": [],
            "monitored": True,
            "education_institute_number": 0,
            "stats_active": True,
            "white_label_file_name": "null",
            "routed_network": True,
            "deal_url": "null",
            "description": "",
            "allow_public_source_ip": False,
            "classroom_exceptions": [],
            "user_defined_name": "null",
            "active": True,
            "mylinewize_login": "null",
            "paid_subscription": False,
            "reseller": "null",
            "install_date": "null",
            "classroom_allow_owner_access": False,
            "failover_active": False,
            "customer_type": "null",
            "deviceid": "testdevice1",
            "surfwize": False,
            "inventory": None,
            "update_allow_auto": True,
            "update_branch": "stable",
            "classroom_groups_group_prefix": None,
            "classroom_restrict_global_teachers": False,
            "classwize_reliever_enabled": False,
            "xero_id": "null",
            "msp": "null",
            "watchdog_recipients": []
        }

        device2 = {
            "key": "null",
            "last_version": "null",
            "labels": [],
            "hardware": "null",
            "report_emails": "null",
            "invoice_number": 0,
            "edgewize": False,
            "timezone": "null",
            "beta_tester": False,
            "classroom_groups": [],
            "monitored": True,
            "education_institute_number": 0,
            "stats_active": True,
            "white_label_file_name": "null",
            "routed_network": True,
            "deal_url": "null",
            "description": "",
            "allow_public_source_ip": False,
            "classroom_exceptions": [],
            "user_defined_name": "null",
            "active": True,
            "mylinewize_login": "null",
            "paid_subscription": False,
            "reseller": "null",
            "install_date": "null",
            "classroom_allow_owner_access": False,
            "failover_active": False,
            "customer_type": "null",
            "deviceid": "testdevice2",
            "surfwize": False,
            "inventory": None,
            "update_allow_auto": True,
            "update_branch": "stable",
            "classroom_groups_group_prefix": None,
            "classroom_restrict_global_teachers": False,
            "classwize_reliever_enabled": False,
            "xero_id": "null",
            "msp": "null",
            "watchdog_recipients": []
        }

        devices = [device1, device2]

        httpretty.register_uri(
            httpretty.GET, uri="http://accountmanagementserviceurl/device", body=json.dumps(dict(result=devices)))

        handler = DeviceConfigHandler(config, 'my_app', engage=False)

        handler.update_all_devices()

        self.assertEquals(device1, handler.devices.get("testdevice1"))
        self.assertEquals(device2, handler.devices.get("testdevice2"))
