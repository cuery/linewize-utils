from base64 import urlsafe_b64encode


def authorize_header(key_id, key_secret, headers=None):
    """ Creates Authorization header for basic http auth.
    :param key_id: Key id value for basic http auth.
    :param key_secret: Key secret value for basic http auth.
    :param headers: Optional existing headers. Authorization header will be appended or overwritten.
    :returns: Headers dict with Authorization base http header url safe base64 encoded.
    """
    if not headers:
        headers = {}
    if key_id and key_secret:
        headers['Authorization'] = "Basic " + urlsafe_b64encode(key_id + ':' + key_secret)
    return headers
