import json
from unittest import TestCase
import httpretty
from lwutils.common_model import CloudDevice, CloudUser
from lwutils.accountmanagementservice_client import AccountManagementPersistenceService

__author__ = 'Cody Harrington'
__email__ = 'cody.harrington@linewize.com'


class TestAccountManagementPersistenceService(TestCase):
# If these tests are breaking, check that the accountmanagementservice address and port haven't changed.

    def setUp(self):
        self.ams_url = "http://localhost:5008"
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def httpretty_mock(self, request_type, uri, response_body, status_code=200):
        httpretty.register_uri(request_type, "{}/{}".format(self.ams_url, uri), json.dumps(response_body), status=status_code)

    @httpretty.activate
    def test_getaccount(self):

        response = {"result": {
            "email": "james",
            "customerid": 11
        }}

        self.httpretty_mock(httpretty.GET, "account/11", response_body=response)

        expected = CloudUser()
        expected.load_attributes_from_dict(response["result"])
        actual = AccountManagementPersistenceService.get_account(self.ams_url, 11)

        self.assertEqual(expected.customerid, actual.customerid)
        self.assertEqual(expected.email, actual.email)
        self.assertEqual(expected.password, actual.password)

    @httpretty.activate
    def test_getaccountbyemail(self):
        response = {"result": {
            "email": "james",
            "customerid": 11
        }}

        self.httpretty_mock(httpretty.GET, "account/email/james", response_body=response)

        expected = CloudUser()
        expected.load_attributes_from_dict(response["result"])
        actual = AccountManagementPersistenceService.get_account_by_email(self.ams_url, "james")

        self.assertEqual(expected.customerid, actual.customerid)
        self.assertEqual(expected.email, actual.email)
        self.assertEqual(expected.password, actual.password)

    @httpretty.activate
    def test_get_all_accounts(self):
        response = {"result": [{
            "email": "james",
            "customerid": 11
        }, {
            "email": "john",
            "customerid": 12
        }, {
            "email": "jim",
            "customerid": 13
        }]
        }

        self.httpretty_mock(httpretty.GET, "account", response_body=response)
        expected_list = []
        for account_dict in response["result"]:
            acc = CloudUser()
            acc.load_attributes_from_dict(account_dict)
            expected_list.append(acc)

        result = AccountManagementPersistenceService.get_all_accounts(self.ams_url)

        for (expected, actual) in zip(expected_list, result):
            self.assertEqual(expected.customerid, actual.customerid)
            self.assertEqual(expected.email, actual.email)
            self.assertEqual(expected.password, actual.password)

    @httpretty.activate
    def test_getdevice(self):
        response = {"result": {
            "deviceid": "testdevice1",
            "description": "",
            "key": None,
            "accounts": [
                {
                    "email": "james",
                    "customerid": 11
                    }
            ],
            "user_defined_name": None,
            "user_defined_authentication_message": None
        }}

        self.httpretty_mock(httpretty.GET, "device/testdevice1", response_body=response)

        expected_device = CloudDevice()
        expected_device.load_attributes_from_dict(response["result"])
        device = AccountManagementPersistenceService.get_device(self.ams_url, "testdevice1")

        self.assertEqual(device.deviceid, expected_device.deviceid)
        self.assertEqual(device.description, expected_device.description)
        self.assertEqual(device.key, expected_device.key)
        self.assertEqual(device.user_defined_name, expected_device.user_defined_name)

    @httpretty.activate
    def test_get_all_devices(self):
        response = {"result": [{
            "deviceid": "testdevice1",
            "description": "",
            "key": None,
            "user_defined_name": None,
        }, {
            "deviceid": "testdevice2",
            "description": "",
            "key": None,
            "user_defined_name": None,
        }, {
            "deviceid": "testdevice3",
            "description": "",
            "key": None,
            "user_defined_name": None,
        }]}

        self.httpretty_mock(httpretty.GET, "device", response_body=response)

        expected_device_list = []
        for device_dict in response["result"]:
            d = CloudDevice()
            d.load_attributes_from_dict(device_dict)
            expected_device_list.append(d)

        result = AccountManagementPersistenceService.get_all_devices(self.ams_url)

        for (expected_device, device) in zip(expected_device_list, result):
            self.assertEqual(device.deviceid, expected_device.deviceid)
            self.assertEqual(device.description, expected_device.description)
            self.assertEqual(device.key, expected_device.key)

    @httpretty.activate
    def test_add_new_account(self):
        account_dict = {
            "result": {
                "email": "james",
                "customerid": 11
            }}

        account_to_add = CloudUser()
        account_to_add.load_attributes_from_dict(account_dict["result"])

        self.httpretty_mock(httpretty.PUT, "account", response_body=account_dict)

        response = AccountManagementPersistenceService.add_new_account(self.ams_url, account_to_add)
        self.assertTrue(response)
        self.assertEqual(account_to_add.customerid, 11)

    @httpretty.activate
    def test_add_new_device(self):
        device_dict = {
            "result": {
                "deviceid": "testdevice1",
                "description": "",
                "key": None,
                "accounts": [],
                "user_defined_name": None,
            }}

        device_to_add = CloudDevice()
        device_to_add.load_attributes_from_dict(device_dict["result"])

        self.httpretty_mock(httpretty.PUT, "device", response_body=device_dict)

        response = AccountManagementPersistenceService.add_new_device(self.ams_url, device_to_add)

        self.assertTrue(response)
        self.assertEqual(device_to_add.deviceid, "testdevice1")

    @httpretty.activate
    def test_authenticate(self):
        response_data = {"result": {
            "email": "james",
            "customerid": 11
        }}

        self.httpretty_mock(httpretty.POST, "authenticate", response_body=response_data)
        expected = CloudUser()
        expected.load_attributes_from_dict(response_data["result"])

        actual = AccountManagementPersistenceService.authenticate(self.ams_url, "james", "testpassword")

        self.assertEqual(expected.customerid, actual.customerid)
        self.assertEqual(expected.email, actual.email)
        self.assertEqual(expected.password, actual.password)

    @httpretty.activate
    def test_delete_account(self):
        mocked_response = {
            "result": ""
        }
        self.httpretty_mock(httpretty.DELETE, "account/1", response_body=mocked_response)
        response = AccountManagementPersistenceService.delete_account(self.ams_url, 1)
        self.assertTrue(response)

    @httpretty.activate
    def test_delete_account_error(self):
        mocked_response = {
            "error": {
                "causing_application": "someapp",
                "exception": "someexception",
                "from_url": "aa",
                "to_url": "bb",
                "to_status_code": 500,
                "message": "",
                "device_id": "somedevice"
            }
        }
        self.httpretty_mock(httpretty.DELETE, "account/1", response_body=mocked_response, status_code=500)
        response = AccountManagementPersistenceService.delete_account(self.ams_url, 1)
        self.assertFalse(response)

    @httpretty.activate
    def test_delete_device(self):
        mocked_response = {
            "result": ""
        }
        self.httpretty_mock(httpretty.DELETE, "device/testdevice1", response_body=mocked_response)
        response = AccountManagementPersistenceService.delete_device(self.ams_url, "testdevice1")
        self.assertTrue(response)

    @httpretty.activate
    def test_delete_device_error(self):
        mocked_response = {
            "error": {
                "causing_application": "someapp",
                "exception": "someexception",
                "from_url": "aa",
                "to_url": "bb",
                "to_status_code": 500,
                "message": "",
                "device_id": "somedevice"
            }
        }

        self.httpretty_mock(httpretty.DELETE, "device/1", response_body=mocked_response, status_code=500)
        response = AccountManagementPersistenceService.delete_device(self.ams_url, 1)
        self.assertFalse(response)

    @httpretty.activate
    def test_modify_account(self):
        mocked_response = {
            "result": "result string"
        }

        self.httpretty_mock(httpretty.POST, "account/1", response_body=mocked_response)
        acc = CloudUser(1, "testemail", "testpassword", True)
        acc.devices = [CloudDevice("testdevice1")]
        response = AccountManagementPersistenceService.update_existing_account(self.ams_url, acc)
        self.assertTrue(response)

    @httpretty.activate
    def test_modify_device(self):
        mocked_response = {
            "result": "result string"
        }

        self.httpretty_mock(httpretty.POST, "device/testdevice1", response_body=mocked_response)
        dev = CloudDevice("testdevice1")
        response = AccountManagementPersistenceService.update_existing_device(self.ams_url, dev)
        self.assertTrue(response)
