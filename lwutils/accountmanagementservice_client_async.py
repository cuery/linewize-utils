import json
from lwutils.common_model import CloudUser, CloudDevice, CloudDeviceStats
from tornado.httpclient import AsyncHTTPClient
from tornado import gen


def format_request_arguments(request_arguments):
    resp = ""
    for key, values in request_arguments.items():
        for value in values:
            resp += "?" if not resp else "&"
            resp += key + "=" + value
    return resp


@gen.coroutine
def fetch_coroutine(url, **kwargs):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url, **kwargs)
    raise gen.Return(response)


class InterApplicationException(Exception):
    def __init__(self, causing_application, exception, from_url=None, to_url=None, to_status_code=None, message=None, device_id=None):
        self.causing_application = causing_application
        self.exception = exception
        self.from_url = from_url
        self.to_url = to_url
        self.status_code = to_status_code
        self.message = message
        self.device_id = device_id
        self.stack_trace = None

    def __str__(self):
        return json.dumps(self.__dict__)


class AsyncAccountManagementPersistenceService():

    @staticmethod
    @gen.coroutine
    def __get_json(url, device_id=None):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if device_id:
            url += "?deviceid=" + device_id
        response = yield fetch_coroutine(url, headers=headers)
        if response.error:
            raise InterApplicationException("accountmanagementpersistenceservice_client_async", response.reason,
                                            device_id=device_id, from_url=url, to_url=response.effective_url, to_status_code=response.code)
        raise gen.Return(json.loads(response.body))

    @staticmethod
    @gen.coroutine
    def get_all_devices(service_url):
        response = yield AsyncAccountManagementPersistenceService.__get_json("{}/device".format(service_url))
        devices = []
        for device_dict in response.get("result"):
            dev = CloudDevice()
            dev.load_attributes_from_dict(device_dict)
            devices.append(dev)
        raise gen.Return(devices)

    @staticmethod
    @gen.coroutine
    def get_device(service_url, deviceid):
        response = yield AsyncAccountManagementPersistenceService.__get_json(
            "{}/device/{}".format(service_url, deviceid), device_id=deviceid)
        dev = CloudDevice()
        dev.load_attributes_from_dict(response["result"])
        raise gen.Return(dev)

    @staticmethod
    @gen.coroutine
    def get_applications(service_url):
        response = yield AsyncAccountManagementPersistenceService.__get_json("{}/applications".format(service_url))
        raise gen.Return(response.get("result"))

    @staticmethod
    @gen.coroutine
    def get_application(service_url, application_id):
        response = yield AsyncAccountManagementPersistenceService.__get_json(
            "{}/application/{}".format(service_url, application_id))
        raise gen.Return(response.get("result"))

    @staticmethod
    @gen.coroutine
    def get_device_stats(service_url, deviceid):
        response = yield AsyncAccountManagementPersistenceService.__get_json("{}/device/{}/stats".format(service_url, deviceid))
        dev_stats = CloudDeviceStats()
        dev_stats.load_attributes_from_dict(response["result"])
        raise gen.Return(dev_stats)

    @staticmethod
    @gen.coroutine
    def get_account_permissions(ams_url, accountid):
        response = yield AsyncAccountManagementPersistenceService.__get_json("{}/account/{}/permissions".format(ams_url, accountid))
        raise gen.Return(response.get("result"))