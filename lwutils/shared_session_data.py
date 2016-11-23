SESSION_DEVICE_ID_KEY = "DEVICEID"
SESSION_TOKEN_KEY = "token"
SESSION_SPHIREWALL_USER_NAME = "username"
SESSION_SPHIREWALL_MAC = "mac"
SESSION_SPHIREWALL_IP = "ip"
SESSION_CLASSROOM_MANAGER_GROUP = "group"
SESSION_CLASSROOM_MANAGER_RELIEVE = "relieve"


def session_get_token(flask_session_dict):
    return flask_session_dict.get(SESSION_TOKEN_KEY)


def session_get_deviceid(flask_session_dict):
    return flask_session_dict.get(SESSION_DEVICE_ID_KEY)


def session_set_token(flask_session_dict, token):
    flask_session_dict[SESSION_TOKEN_KEY] = token


def session_set_deviceid(flask_session_dict, deviceid):
    flask_session_dict[SESSION_DEVICE_ID_KEY] = deviceid


def session_set_sphirewall_username(flask_session_dict, sphirewall_username):
    flask_session_dict[SESSION_SPHIREWALL_USER_NAME] = sphirewall_username


def session_get_sphirewall_username(flask_session_dict):
    return flask_session_dict.get(SESSION_SPHIREWALL_USER_NAME)


def session_set_source_mac_address(flask_session_dict, mac_address):
    flask_session_dict[SESSION_SPHIREWALL_MAC] = mac_address


def session_set_source_ip(flask_session_dict, ip):
    flask_session_dict[SESSION_SPHIREWALL_IP] = ip


def session_get_source_mac_address(flask_session_dict):
    return flask_session_dict.get(SESSION_SPHIREWALL_MAC)


def session_get_source_ip(flask_session_dict):
    return flask_session_dict.get(SESSION_SPHIREWALL_IP)


def session_get_classroom_manager_group(flask_session_dict):
    return flask_session_dict.get(SESSION_CLASSROOM_MANAGER_GROUP)


def session_set_classroom_manager_group(flask_session_dict, group):
    flask_session_dict[SESSION_CLASSROOM_MANAGER_GROUP] = group


def session_get_classroom_manager_relieve(flask_session_dict):
    return flask_session_dict.get(SESSION_CLASSROOM_MANAGER_RELIEVE)


def session_set_classroom_manager_relieve(flask_session_dict, relieve):
    flask_session_dict[SESSION_CLASSROOM_MANAGER_RELIEVE] = relieve
