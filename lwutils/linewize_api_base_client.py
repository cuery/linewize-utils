from datetime import datetime
import ujson as json
import requests
from lwutils.sphirewall_connection import ApiDispatcherTransportProvider
from sphirewallapi.sphirewall_api import SphirewallClient
from lwutils.authorization_utils import authorize_header
from lwutils.error_handler import error_handled_response


class DevicePermissionException(Exception):

    def __init__(self, message, *args, **kwargs):
        super(DevicePermissionException, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        return repr("DevicePermissionException Exception: message: '%s'" % self.message)


class InvalidUserSession(Exception):

    def __init__(self, message, *args, **kwargs):
        super(InvalidUserSession, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        return repr("InvalidUserSession Exception: message: '%s'" % self.message)


class GeneralServiceError(Exception):

    def __init__(self, response, *args, **kwargs):
        super(GeneralServiceError, self).__init__(*args, **kwargs)
        try:
            self.message = json.loads(response)["err"]
        except:
            self.message = response

    def __str__(self):
        return repr("GeneralServiceError Exception: message: '%s'" % self.message)


class LinewizeApiClient(object):

    _service_url = None
    _application_key_id = None
    _application_key_secret = None
    _session_token = None

    def __init__(self, service_url, application_key_id, application_key_secret, session_token=None, app_name=None):
        self._service_url = service_url
        self._application_key_id = application_key_id
        self._application_key_secret = application_key_secret
        self._session_token = session_token
        self._app_name = app_name

    def _handle_json_response(self, response):
        return json.loads(self._handle_response(response).text)

    def _handle_response(self, response):
        if response.status_code == 401:
            raise InvalidUserSession("Invalid user session")
        if response.status_code == 403:
            raise DevicePermissionException("Permission denied")
        elif response.status_code != 200:
            raise GeneralServiceError(response.text)
        return response

    def put_json(self, url, data, _device_id=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret,
                                   {'Content-type': 'application/json', 'Accept': 'text/plain'})
        params = {"access_token": self._session_token, 'deviceid': _device_id}

        response = error_handled_response(self._app_name, requests.put(
            "{}{}".format(self._service_url, url), data=json.dumps(data), headers=headers, params=params))
        return self._handle_json_response(response)

    def delete_json(self, url, _device_id=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret,
                                   {'Content-type': 'application/json', 'Accept': 'text/plain'})
        params = {"access_token": self._session_token, 'deviceid': _device_id}

        response = error_handled_response(self._app_name, requests.delete(
            "{}{}".format(self._service_url, url), headers=headers, params=params))
        return self._handle_json_response(response)

    def post_json(self, url, data, _device_id=None, whitelabel=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret,
                                   {'Content-type': 'application/json', 'Accept': 'text/plain'})
        params = {"access_token": self._session_token, 'deviceid': _device_id, 'whitelabel': whitelabel}

        response = error_handled_response(self._app_name, requests.post(
            "{}{}".format(self._service_url, url), data=json.dumps(data), headers=headers, params=params))
        return self._handle_json_response(response)


    def post_json_no_parsing(self, url, data, _device_id=None, whitelabel=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret,
                                   {'Content-type': 'application/json', 'Accept': 'text/plain'})
        params = {"access_token": self._session_token, 'deviceid': _device_id, 'whitelabel': whitelabel}

        response = error_handled_response(self._app_name, requests.post(
            "{}{}".format(self._service_url, url), data=json.dumps(data), headers=headers, params=params))
        version = response.headers.get("Config-Version", "")
        return self._handle_response(response), version

    def post_json_file(self, url, data, _device_id=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret,
                                   {'Content-type': 'application/json', 'Accept': 'text/plain'})
        params = {"access_token": self._session_token, 'deviceid': _device_id}

        response = error_handled_response(self._app_name, requests.post(
            "{}{}".format(self._service_url, url), data=json.dumps(data), headers=headers, params=params))
        return response

    def get_json(self, url, params=None, _device_id=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret,
                                   {'Content-type': 'application/json', 'Accept': 'text/plain'})
        if not params:
            params = {}
        params["access_token"] = self._session_token
        params['deviceid'] = _device_id

        response = error_handled_response(
            self._app_name, requests.get("{}{}".format(self._service_url, url), headers=headers, params=params))
        return self._handle_json_response(response)

    def get(self, url, params=None, _device_id=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret,
                                   {'Content-type': 'application/json', 'Accept': 'text/plain'})
        if not params:
            params = {}
        params["access_token"] = self._session_token
        params['deviceid'] = _device_id

        response = error_handled_response(
            self._app_name, requests.get("{}{}".format(self._service_url, url), headers=headers, params=params))
        return self._handle_response(response)

    def analytics_query(self, url, filter_user=None, filter_group=None, filter_period=None, filter_category=None, filter_mac=None,
                        filter_ip=None, startDate=None, endDate=None, startTime=None, endTime=None, limit=None, offset=None, search=None, event=None,
                        include_noise=None, include_blocked_flag=False, _device_id=None, period=None, interval_start=None, interval_end=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret)
        params = {}
        if startDate is not None:
            params['startDate'] = datetime.strftime(startDate, '%Y-%m-%d')
        if endDate is not None:
            params['endDate'] = datetime.strftime(endDate, '%Y-%m-%d')
        if startTime is not None:
            params['startTime'] = startTime
        if endTime is not None:
            params['endTime'] = endTime
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search is not None:
            params['search'] = search
        if event is not None:
            params['event'] = event
        if filter_category is not None:
            params['filter_category'] = filter_category
        if filter_user is not None:
            params['filter_user'] = filter_user
        if filter_group is not None:
            params['filter_group'] = filter_group
        if filter_mac is not None:
            params['filter_mac'] = filter_mac
        if filter_ip is not None:
            params['filter_ip'] = filter_ip
        if filter_period is not None:
            params['filter_period'] = filter_period
        if include_noise is not None:
            params['include_noise'] = include_noise
        if include_blocked_flag is not None:
            params['include_blocked_flag'] = include_blocked_flag
        if period is not None:
            params['period'] = period
        if interval_start is not None:
            params['interval_start'] = interval_start
        if interval_end is not None:
            params['interval_end'] = interval_end

        params["access_token"] = self._session_token
        params["deviceid"] = _device_id
        try:
            r = error_handled_response(self._app_name, requests.get(
                "{}{}".format(self._service_url, url), headers=headers, params=params))
            json_loads = json.loads(r.text)
            return json_loads["result"]
        except:
            return False

    def analytics_post_query(self, url, data, filter_user=None, filter_group=None, filter_period=None, filter_category=None, filter_mac=None,
                        filter_ip=None, startDate=None, endDate=None, startTime=None, endTime=None, limit=None, offset=None, search=None, event=None,
                        include_noise=None, include_blocked_flag=False, _device_id=None, period=None, interval_start=None, interval_end=None, whitelabel=None):
        headers = authorize_header(self._application_key_id, self._application_key_secret, {'Content-type': 'application/json', 'Accept': 'text/plain'})
        params = {}
        if startDate is not None:
            params['startDate'] = datetime.strftime(startDate, '%Y-%m-%d')
        if endDate is not None:
            params['endDate'] = datetime.strftime(endDate, '%Y-%m-%d')
        if startTime is not None:
            params['startTime'] = startTime
        if endTime is not None:
            params['endTime'] = endTime
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search is not None:
            params['search'] = search
        if event is not None:
            params['event'] = event
        if filter_category is not None:
            params['filter_category'] = filter_category
        if filter_user is not None:
            params['filter_user'] = filter_user
        if filter_group is not None:
            params['filter_group'] = filter_group
        if filter_mac is not None:
            params['filter_mac'] = filter_mac
        if filter_ip is not None:
            params['filter_ip'] = filter_ip
        if filter_period is not None:
            params['filter_period'] = filter_period
        if include_noise is not None:
            params['include_noise'] = include_noise
        if include_blocked_flag is not None:
            params['include_blocked_flag'] = include_blocked_flag
        if period is not None:
            params['period'] = period
        if interval_start is not None:
            params['interval_start'] = interval_start
        if interval_end is not None:
            params['interval_end'] = interval_end
        if whitelabel is not None:
            params['whitelabel'] = whitelabel

        params["access_token"] = self._session_token
        params["deviceid"] = _device_id

        try:
            r = error_handled_response(self._app_name, requests.post(
                "{}{}".format(self._service_url, url), data=json.dumps(data), headers=headers, params=params))

            json_loads = json.loads(r.text)
            return json_loads
        except Exception as e:
            return False

    def sphirewall(self, current_device_id, ignore_missing=False):
        ret = SphirewallClient(
            ApiDispatcherTransportProvider(
                self._service_url, self._application_key_id, self._application_key_secret, current_device_id, self._session_token)
        )
        ret.connection.ignore_missing = ignore_missing
        return ret
