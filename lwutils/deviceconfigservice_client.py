import json
import requests


class DeviceConfigurationPutFailedException(Exception):

    def __init__(self, message, *args, **kwargs):
        super(DeviceConfigurationPutFailedException, self).__init__(*args, **kwargs)
        self.message = message


class DeviceConfigurationSyncFailedException(Exception):

    def __init__(self, message, *args, **kwargs):
        super(DeviceConfigurationSyncFailedException, self).__init__(*args, **kwargs)
        self.message = message


class DeviceConfigurationPersistanceService():

    @staticmethod
    def get(service_url, deviceid):
        r = requests.get(service_url + "/device/" + deviceid)
        parsed_object = json.loads(r.text)
        if "err" in parsed_object:
            return None
        else:
            return parsed_object

    @staticmethod
    def put(service_url, deviceid, device):
        device['requirespublish'] = True
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(service_url + "/device/" + deviceid + "/save",
                                 data=json.dumps(dict(device)), headers=headers)

        parsed_object = json.loads(response.text)
        if "err" in parsed_object:
            raise DeviceConfigurationPutFailedException(parsed_object["err"])

    @staticmethod
    def publish(service_url, device_id):
        response = requests.get("%s/device/%s/publish" % (service_url, device_id))
        return json.loads(response.text)

    @staticmethod
    def create(service_url, device_id):
        response = requests.get("%s/device/%s/create" % (service_url, device_id))
        return json.loads(response.text)
