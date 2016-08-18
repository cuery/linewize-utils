import json
import requests


class LinewizeAgentClient:
    def __init__(self, device_id, key, hostname, port):
        self.device_id = device_id
        self.key = key
        self.hostname = hostname
        self.port = port

    def __send_request(self, type, args):
        if args is None:
            args = {}

        args_ = json.dumps({'request': type, 'args': args})
        data = {'key': self.key, 'deviceid': self.device_id, 'request': args_}

        res = requests.post('https://' + self.hostname + ':' + str(self.port), data=json.dumps(dict(data)), verify=False)

        if res.status_code != 200:
            return None
        return res.json()

    def status(self):
        return self.__send_request("status", {})

    def update(self):
        return self.__send_request("update", {})

    def restart(self):
        return self.__send_request("restart", {})

    def rpc(self, command):
        return self.__send_request("rpc", {"command": command})

    def dump(self):
        return self.__send_request("dump", {})
