import json
import requests
from lwutils.authorization_utils import authorize_header


class ScloudManagerException(Exception):
    ERR_UNKNOWN_DEVICE = 101
    ERR_INVALID_REQUEST_CREDENTIALS = 102
    ERR_REQUEST_ERR = 103
    ERR_REQUEST_SIZE_EXCEEDED = 104
    ERR_INVALID_REQUEST = 105
    ERR_DEVICE_INTERNAL = 106
    ERR_INVALID_RESPONSE = 107

    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code


class ScloudManagerDirectTransportProvider:

    """ This is a TransportProvider for the Sphirewall API.

        It connects to the scloud manager, wraps the passed sphirewall request, then passes it with a key
        and deviceid to the scloud manager. Any exceptions thrown here will be caught by the sphirewall api
        and presented as a TransportProviderException.
     """

    def __init__(self, hostname, port, deviceid, devicekey):
        self.hostname = hostname
        self.port = port
        self.deviceid = deviceid
        self.devicekey = devicekey

    def send(self, input_request_data_dict):
        data = {'key': self.devicekey, 'deviceid': self.deviceid, 'request': json.dumps(input_request_data_dict)}
        res = requests.post('https://' + self.hostname + ':' + str(self.port), timeout=300, data=json.dumps(data), verify=False)
        if res.status_code is not 200:
            json_response = json.loads(res)
            raise ScloudManagerException(json_response["message"], json_response["err"])
        return res.text


class ApiDispatcherTransportProvider:

    """ This is a TransportProvider for the Sphirewall API.

        It connects to the apidispatcher, wraps the passed sphirewall request, then passes it with a
        deviceid to the api dispatcher. Any exceptions thrown here will be caught by the sphirewall api
        and presented as a TransportProviderException.
     """

    def __init__(self, url, application_key_id, application_key_secret, deviceid, session_token=None):
        self.url = url
        self.session_token = session_token
        self.application_key_id = application_key_id
        self.application_key_secret = application_key_secret
        self.deviceid = deviceid

    def send(self, input_request_data_dict):
        sp_request_uri = input_request_data_dict["request"]
        sp_request_args = input_request_data_dict["args"]

        headers = authorize_header(self.application_key_id, self.application_key_secret)
        url = "%s/device/%s/request/%s" % (self.url, self.deviceid, sp_request_uri)

        if self.session_token:
            url += "?access_token=%s" % self.session_token
        rv = requests.post(url, headers=headers, timeout=300, data=json.dumps(sp_request_args))

        if rv.status_code is not 200:
            json_response = json.loads(rv.text)
            raise Exception(json_response["message"], json_response["err"])
        return rv.text
