import time
from lwutils.common_model import CloudUser, CloudDevice, CloudDeviceStats
import requests
import json
from error_handler import error_handled_response


__author__ = 'Cody Harrington'
__email__ = 'cody.harrington@linewize.com'


class AccountManagementPersistenceServiceException(Exception):

    def __init__(self, message, *args, **kwargs):
        super(AccountManagementPersistenceServiceException, self).__init__(*args, **kwargs)
        self.message = message


class AccountManagementPersistenceService():

    @staticmethod
    def __put_json(url, data, device_id=None):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = error_handled_response('accountmanagementpersistenceservice', requests.put(
            url=url, data=json.dumps(data), headers=headers, params={'deviceid': device_id}))
        return json.loads(response.text)

    @staticmethod
    def __delete_json(url, device_id=None):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = error_handled_response('accountmanagementpersistenceservice', requests.delete(
            url=url, headers=headers, params={'deviceid': device_id}))
        return json.loads(response.text)

    @staticmethod
    def __post_json(url, data, device_id=None):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = error_handled_response('accountmanagementpersistenceservice', requests.post(
            url=url, data=json.dumps(data), headers=headers, params={'deviceid': device_id}))
        return json.loads(response.text)

    @staticmethod
    def __get_json(url, device_id=None):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = error_handled_response('accountmanagementpersistenceservice', requests.get(
            url=url, headers=headers, params={'deviceid': device_id}))
        return json.loads(response.text)

    @staticmethod
    def get_account(service_url, customerid):
        try:
            response = AccountManagementPersistenceService.__get_json("{}/account/{}".format(service_url, customerid))
            account = CloudUser()
            account.load_attributes_from_dict(response["result"])
            return account
        except:
            return None

    @staticmethod
    def get_account_metadata(service_url, customerid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/account/{}/metadata".format(service_url, customerid))
        return response["result"]

    @staticmethod
    def get_account_by_email(service_url, email):
        response = AccountManagementPersistenceService.__get_json("{}/account/email/{}".format(service_url, email))
        account = CloudUser()
        account.load_attributes_from_dict(response["result"])
        return account

    @staticmethod
    def get_device(service_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}".format(service_url, deviceid), device_id=deviceid)
        dev = CloudDevice()
        dev.load_attributes_from_dict(response["result"])
        return dev

    @staticmethod
    def get_mylinewize_user_group_mapping(service_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/mylinewize_user_group_mapping".format(service_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def get_device_watchdog(service_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/watchdog/{}".format(service_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def get_device_watchdog_byid(service_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/watchdog/byid/{}".format(service_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def get_all_accounts(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/account".format(service_url))
        accounts = []
        for account_dict in response["result"]:
            acc = CloudUser()
            acc.load_attributes_from_dict(account_dict)
            accounts.append(acc)
        return accounts

    @staticmethod
    def get_all_devices(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/device".format(service_url))
        devices = []
        for device_dict in response["result"]:
            dev = CloudDevice()
            dev.load_attributes_from_dict(device_dict)
            devices.append(dev)
        return devices

    @staticmethod
    def get_all_devices_stats(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/devices/stats".format(service_url))
        devices = []
        for device_stats_dict in response["result"]:
            dev = CloudDeviceStats()
            dev.load_attributes_from_dict(device_stats_dict)
            devices.append(dev)
        return devices

    @staticmethod
    def get_device_stats(service_url, deviceid):
        response = AccountManagementPersistenceService.__get_json("{}/device/{}/stats".format(service_url, deviceid))
        dev_stats = CloudDeviceStats()
        dev_stats.load_attributes_from_dict(response["result"])
        return dev_stats

    @staticmethod
    def get_all_reportrecipients(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/reportrecipients".format(service_url))
        return response["result"]

    @staticmethod
    def get_inventory(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/inventory".format(service_url))
        return response["result"]

    @staticmethod
    def get_updates(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/updates".format(service_url))
        return response["result"]

    @staticmethod
    def get_updates_item(service_url, update_id):
        response = AccountManagementPersistenceService.__get_json(
            "{}/updates/{}".format(service_url, update_id))
        return response["result"]

    @staticmethod
    def get_inventory_item(service_url, serialnumber):
        response = AccountManagementPersistenceService.__get_json("{}/inventory/{}".format(service_url, serialnumber))
        return response["result"]

    @staticmethod
    def add_new_account(service_url, cloud_account):
        data = cloud_account.to_dict()
        response = AccountManagementPersistenceService.__put_json("{}/account".format(service_url), data=data)
        cloud_account.customerid = int(response["result"]["customerid"])
        return True

    @staticmethod
    def add_new_inventory(service_url, cloud_account):
        response = AccountManagementPersistenceService.__put_json(
            "{}/inventory".format(service_url), data=cloud_account)
        return True

    @staticmethod
    def add_business_metric(service_url, metric):
        AccountManagementPersistenceService.__put_json("{}/busmetrics".format(service_url), data=metric)
        return True

    @staticmethod
    def get_business_metric(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/busmetrics".format(service_url))
        return response

    @staticmethod
    def update_existing_inventory(service_url, serialnumber, cloud_account):
        response = AccountManagementPersistenceService.__post_json(
            "{}/inventory/{}".format(service_url, serialnumber), data=cloud_account)
        return True

    @staticmethod
    def add_new_updates(service_url, item):
        response = AccountManagementPersistenceService.__put_json("{}/updates".format(service_url), data=item)
        return True

    @staticmethod
    def update_existing_updates(service_url, update_id, item):
        response = AccountManagementPersistenceService.__post_json(
            "{}/updates/{}".format(service_url, update_id), data=item)
        return True

    @staticmethod
    def add_new_device(service_url, cloud_device):
        data = cloud_device.to_dict()
        response = AccountManagementPersistenceService.__put_json("{}/device".format(service_url), data=data)
        cloud_device.deviceid = response["result"]["deviceid"]
        return True

    @staticmethod
    def update_existing_account(service_url, cloud_account):
        data = cloud_account.to_dict()
        response = AccountManagementPersistenceService.__post_json(
            "{}/account/{}".format(service_url, cloud_account.customerid), data=data)
        return True

    @staticmethod
    def update_existing_device_physical(service_url, cloud_device):
        data = cloud_device.to_dict()
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/physical/{}".format(service_url, cloud_device.deviceid), data=data, device_id=deviceid)
        return True

    @staticmethod
    def update_existing_device_physical(service_url, device_id_, cloud_device):
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/watchdog/{}".format(service_url, device_id_), data=cloud_device, device_id=device_id_)
        return True

    @staticmethod
    def update_existing_device(service_url, cloud_device):
        data = cloud_device.to_dict()
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/{}".format(service_url, cloud_device.deviceid), data=data, device_id=cloud_device.deviceid)
        return True

    @staticmethod
    def update_existing_device_no_notification(service_url, cloud_device):
        data = cloud_device.to_dict()
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/{}/no_notification".format(service_url, cloud_device.deviceid), data=data, device_id=cloud_device.deviceid)
        return True

    @staticmethod
    def update_existing_device_stats(service_url, device_stats):
        data = device_stats.to_dict()
        AccountManagementPersistenceService.__post_json(
            "{}/device/{}/stats/no_notification".format(service_url, device_stats.deviceid), data=data, device_id=device_stats.deviceid)
        return True

    @staticmethod
    def update_existing_account_metadata(service_url, cloud_account):
        response = AccountManagementPersistenceService.__post_json(
            "{}/account/{}/metadata".format(service_url, cloud_account.customerid), data=cloud_account)
        return True

    @staticmethod
    def create_device_physical(service_url, device_id):
        response = AccountManagementPersistenceService.__put_json(
            "{}/device/physical".format(service_url, device_id), data={"deviceid": device_id})
        return True

    @staticmethod
    def delete_account(service_url, customerid):
        try:
            response = AccountManagementPersistenceService.__delete_json(
                "{}/account/{}".format(service_url, customerid))
            return True
        except:
            return False

    @staticmethod
    def delete_device(service_url, deviceid):
        try:
            response = AccountManagementPersistenceService.__delete_json(
                "{}/device/{}".format(service_url, deviceid), device_id=deviceid)
            return True
        except:
            return False

    @staticmethod
    def delete_physical_device(service_url, deviceid):
        try:
            response = AccountManagementPersistenceService.__delete_json(
                "{}/device/physical/{}".format(service_url, deviceid), device_id=deviceid)
            return True
        except:
            return False

    @staticmethod
    def authenticate(service_url, email, password):
        data = {"email": email, "password": password}
        response = AccountManagementPersistenceService.__post_json("{}/authenticate".format(service_url), data=data)
        acc = CloudUser()
        acc.load_attributes_from_dict(response["result"])
        return acc

    @staticmethod
    def get_all_device_physical(ams_url):
        response = AccountManagementPersistenceService.__get_json("{}/device/physical".format(ams_url))
        return response["result"]

    @staticmethod
    def add_new_device_statistic_snapshot(ams_url, deviceid, state):
        response = AccountManagementPersistenceService.__put_json(
            "{}/device/{}/statistics".format(ams_url, deviceid), data=state, device_id=deviceid)
        return True

    @staticmethod
    def add_new_device_configuration_snapshot(ams_url, deviceid, account, description, snapshot):
        response = AccountManagementPersistenceService.__put_json(
            "{}/device/{}/snapshots".format(ams_url, deviceid), data=dict(account=account, description=description, snapshot=snapshot), device_id=deviceid)
        return True

    @staticmethod
    def get_device_configuration_snapshots(ams_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/snapshots".format(ams_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def get_device_configuration_snapshot(ams_url, deviceid, snapshotid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/snapshots/{}".format(ams_url, deviceid, snapshotid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def add_new_device_watchdog_event(ams_url, deviceid, event):
        data = {"time": time.time(), "event": event, "deviceid": deviceid}
        response = AccountManagementPersistenceService.__put_json(
            "{}/device/{}/events".format(ams_url, deviceid), data=data, device_id=deviceid)
        return True

    @staticmethod
    def get_device_watchdog_events(ams_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/events".format(ams_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def get_statistics(ams_url):
        response = AccountManagementPersistenceService.__get_json("{}/device/statistics".format(ams_url))
        return response["result"]

    @staticmethod
    def get_device_permissions(ams_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/permissions".format(ams_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def get_account_permissions(ams_url, accountid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/account/{}/permissions".format(ams_url, accountid))
        return response["result"]

    @staticmethod
    def set_device_accounts_permissions(ams_url, permission_object):
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/{}/permissions".format(ams_url, permission_object["deviceid"]), data=permission_object, device_id=permission_object["deviceid"])
        return response["result"]

    @staticmethod
    def set_device_accounts(ams_url, permission_object):
        response = AccountManagementPersistenceService.__put_json(
            "{}/device/{}/permissions".format(ams_url, permission_object["deviceid"]), data=permission_object, device_id=permission_object["deviceid"])
        return response["result"]

    @staticmethod
    def get_device_accounts(ams_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/permissions".format(ams_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def get_device_subscription(ams_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/subscription".format(ams_url, deviceid), device_id=deviceid)
        return response["result"]

    @staticmethod
    def update_device_subscription(ams_url, deviceid, entity):
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/{}/subscription".format(ams_url, deviceid), entity, device_id=deviceid)
        return response["result"]

    @staticmethod
    def delete_device_accounts_permissions(ams_url, deviceid, accountid):
        AccountManagementPersistenceService.__delete_json(
            "{}/device/{}/{}/permissions".format(ams_url, deviceid, accountid), device_id=deviceid)

    @staticmethod
    def get_applications(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/applications".format(service_url))
        return response["result"]

    @staticmethod
    def get_application(service_url, application_id):
        response = AccountManagementPersistenceService.__get_json(
            "{}/application/{}".format(service_url, application_id))
        return response["result"]

    @staticmethod
    def add_new_application(service_url, description, cloud_accounts_id, key_id, key_secret, permissions):
        data = {
            "description": description,
            "cloud_accounts_id": cloud_accounts_id,
            "key_id": key_id,
            "key_secret": key_secret,
            "permissions": permissions
        }
        response = AccountManagementPersistenceService.__put_json("{}/application".format(service_url), data=data)
        return response["result"]

    @staticmethod
    def update_application(application_id, service_url, description, cloud_accounts_id, key_id, key_secret, permissions):
        data = {
            "description": description,
            "cloud_accounts_id": cloud_accounts_id,
            "key_id": key_id,
            "key_secret": key_secret,
            "permissions": permissions
        }
        response = AccountManagementPersistenceService.__post_json(
            "{}/application/{}".format(service_url, application_id), data=data)
        return response["result"]

    @staticmethod
    def delete_application(application_id, service_url,):
        response = AccountManagementPersistenceService.__delete_json(
            "{}/application/{}".format(service_url, application_id))
        return True

    @staticmethod
    def get_reporting_filters(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/reportingfilters".format(service_url))
        return response["result"]

    @staticmethod
    def get_reporting_filter(service_url, cloud_account_id):
        response = AccountManagementPersistenceService.__get_json(
            "{}/reportingfilter/{}".format(service_url, cloud_account_id))
        return response["result"]

    @staticmethod
    def add_new_reporting_filter(service_url, description, cloud_account_id, groups, users):
        data = {
            "description": description,
            "cloud_account_id": cloud_account_id,
            "groups": groups,
            "users": users
        }
        response = AccountManagementPersistenceService.__put_json("{}/reportingfilter".format(service_url), data=data)
        return response["result"]

    @staticmethod
    def update_reporting_filter(service_url, description, cloud_account_id, groups, users):
        data = {
            "description": description,
            "groups": groups,
            "users": users
        }
        response = AccountManagementPersistenceService.__post_json(
            "{}/reportingfilter/{}".format(service_url, cloud_account_id), data=data)
        return response["result"]

    @staticmethod
    def delete_reporting_filter(cloud_account_id, service_url,):
        AccountManagementPersistenceService.__delete_json(
            "{}/reportingfilter/{}".format(service_url, cloud_account_id))
        return True

    @staticmethod
    def get_alert_configurations(service_url, device_id):
        response = AccountManagementPersistenceService.__get_json("{}/device/{}/alerts".format(service_url, device_id))
        return response["result"]

    @staticmethod
    def get_scheduler_tasks(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/scheduler/tasks".format(service_url))
        return response["result"]

    @staticmethod
    def get_s3_metadata(service_url, start_day_hour):
        response = AccountManagementPersistenceService.__get_json(
            "{}/s3_metadata/{}".format(service_url, start_day_hour))
        return response["result"]

    @staticmethod
    def get_report_plugins(service_url, name):
        response = AccountManagementPersistenceService.__get_json("{}/report/plugins/{}".format(service_url, name))
        return response["result"]

    @staticmethod
    def update_report_plugins(service_url, name, plugins):
        data = {
            "name": name,
            "plugins": plugins
        }
        response = AccountManagementPersistenceService.__post_json("{}/report/plugins".format(service_url), data=data)
        return response["result"]

    @staticmethod
    def get_report_dynamic_plugin(service_url, name):
        response = AccountManagementPersistenceService.__get_json(
            "{}/report/dynamic/plugin/{}".format(service_url, name))
        return response["result"]

    @staticmethod
    def update_report_dynamic_plugin(service_url, name, content):
        data = {
            "name": name,
            "content": content
        }
        response = AccountManagementPersistenceService.__post_json(
            "{}/report/dynamic/plugin".format(service_url), data=data)
        return response["result"]

    @staticmethod
    def delete_report_dynamic_plugin(service_url, name):
        response = AccountManagementPersistenceService.__delete_json(
            "{}/report/dynamic/plugin/{}".format(service_url, name))
        return response

    @staticmethod
    def get_report_dynamic_plugins(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/report/dynamic/plugins".format(service_url))
        return response["result"]

    @staticmethod
    def get_report_scheduled_pdfs(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/report/scheduled/pdfs".format(service_url))
        return response["result"]

    @staticmethod
    def get_user_object(service_url, deviceid, username):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/configuration/authentication/users/username/{}".format(service_url, deviceid, username))
        return response["result"]

    @staticmethod
    def set_user_object(service_url, deviceid, user_object):
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/{}/configuration/authentication/users".format(service_url, deviceid), data=user_object)
        return response["result"]

    @staticmethod
    def set_captiveportal(service_url, deviceid, cp_object):
        response = AccountManagementPersistenceService.__post_json(
            "{}/device/{}/configuration/authentication/captiveportal".format(service_url, deviceid), data=cp_object)
        return response["result"]

    @staticmethod
    def get_all_msps(service_url):
        response = AccountManagementPersistenceService.__get_json("{}/msps".format(service_url))
        return response["result"]

    @staticmethod
    def get_user_downvotes(service_url, deviceid):
        response = AccountManagementPersistenceService.__get_json(
            "{}/device/{}/user/downvotes".format(service_url, deviceid))
        return response["result"]
