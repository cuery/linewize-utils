from flask.globals import request
from re import match


def checkbox_value(key):
    if key in request.form:
        return True
    return False


def text_value(key, default="", nonvalid=True):
    if key in request.form and len(request.form[key]) > 0:
        return request.form[key]
    return None if nonvalid else default


def int_value(key, default=-1):
    if key in request.form and len(request.form[key]) > 0:
        return int(request.form[key])
    return default


def arg(key, default=None):
    if key in request.args:
        return request.args[key]
    return default


def check_passwords_match(password1, password2):
    return password1 == password2


def check_email_correct_format(email):
    # Note: Does not parse correctly according to RFC5321 and RFC5322!
    regex = "^[a-zA-Z0-9_.]+@[a-zA-Z0-9\-]+(\.[a-zA-Z]{1,3})+$"
    if match(regex, email) is None:
        return False
    return True


def check_fields_empty(*fields):
    for field in fields:
        if field is None or len(field) == 0:
            return True
    return False


def property_is_true(name, blob):
    if name in blob:
        return blob[name]
    return False
