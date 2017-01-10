import json
import unittest
import httpretty
from lwutils.linewize_api_base_client import LinewizeApiClient, GeneralServiceError, InvalidUserSession, DevicePermissionException
from sphirewallapi.sphirewall_api import TransportProviderException
from lwutils.error_handler import InterApplicationException


class LinewizeApiClientTestCase(unittest.TestCase):

    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    @httpretty.activate
    def test_general_error_throws_exception(self):
        httpretty.register_uri(httpretty.GET, "http://localhost/blah", body=json.dumps(dict(err="an error message")), status=500)

        service = LinewizeApiClient("http://localhost", None, None)
        self.assertRaises(InterApplicationException, service.get_json, "/blah")

    @httpretty.activate
    def test_invalid_token_error_throws_exception(self):
        httpretty.register_uri(httpretty.GET, "http://localhost/blah", body=json.dumps(dict(errcode=0)), status=403)

        service = LinewizeApiClient("http://localhost", None, None)
        self.assertRaises(DevicePermissionException, service.get_json, "/blah")

    @httpretty.activate
    def test_invalid_permissions_error_throws_exception(self):
        httpretty.register_uri(httpretty.GET, "http://localhost/blah", body=json.dumps(dict(errcode=1)), status=403)

        service = LinewizeApiClient("http://localhost", None, None)
        self.assertRaises(DevicePermissionException, service.get_json, "/blah")

    @httpretty.activate
    def test_valid_request_returns_dict_response(self):
        httpretty.register_uri(httpretty.GET, "http://localhost/blah", body=json.dumps(dict(result="cool, that worked")), status=200)

        service = LinewizeApiClient("http://localhost", None, None)
        assert service.get_json("/blah") == {"result": "cool, that worked"}

    @httpretty.activate
    def test_cloud_connection_detail(self):
        httpretty.register_uri(httpretty.POST, "http://localhost/device/device1/request/firewall/acls/list", body=json.dumps(dict(response=dict(normal="dude"), code=0)), status=200)

        cc = LinewizeApiClient("http://localhost", "key_id", "key_secret")
        assert cc.sphirewall("device1").firewall().acls() == "dude"

    @httpretty.activate
    def test_cloud_connection_detail_fail_invalid_session(self):
        httpretty.register_uri(httpretty.POST, "http://localhost/device/device1/request/firewall/acls/list?access_token=token", body=json.dumps(dict(errcode=0)), status=403)

        cc = LinewizeApiClient("http://localhost", "key_id", "key_secret")
        sphirewall_client = cc.sphirewall("device1").firewall()

        self.assertRaises(TransportProviderException, sphirewall_client.acls)

    @httpretty.activate
    def test_cloud_connection_detail_fail_permissions(self):
        httpretty.register_uri(httpretty.POST, "http://localhost/device/device1/request/firewall/acls/list?access_token=token", body=json.dumps(dict(errcode=1)), status=403)

        cc = LinewizeApiClient("http://localhost", "key_id", "key_secret")
        sphirewall_client = cc.sphirewall("device1").firewall()

        self.assertRaises(TransportProviderException, sphirewall_client.acls)

    @httpretty.activate
    def test_cloud_connection_detail_another_error(self):
        httpretty.register_uri(httpretty.POST, "http://localhost/device/device1/request/firewall/acls/list?access_token=token", body=json.dumps(dict(err="error message")), status=201)

        cc = LinewizeApiClient("http://localhost", "key_id", "key_secret")
        sphirewall_client = cc.sphirewall("device1").firewall()

        self.assertRaises(TransportProviderException, sphirewall_client.acls)
