import collections
from common_model import *


def get_range(d, begin, end):
    index = 0
    ret = []
    for i in d:
        index += 1
        if index < end:
            ret.append(i)
        else:
            break
    return ret


def sqlalchemy_to_dict(inst, excluded_keys=None):
    result = dict()
    cls = inst.__class__
    for c in cls.__table__.columns:
        result[c.name] = getattr(inst, c.name)
        if excluded_keys is not None and c.name in excluded_keys:
            del result[c.name]
    return result


def first(this_key, from_this, if_this, is_this, defaulting_to_this=None):
    return next((x for x in from_this[this_key] if x[if_this] == is_this), defaulting_to_this)


def flatten_dict(d):
    items = []
    for k, v in d.items():
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v).items())
        else:
            items.append((k, v))
    return dict(items)


def checkEqual(dict_one, dict_two, key):
    if key in dict_one:
        if key in dict_two:
            return dict_one[key] == dict_two[key]
        else:
            return False
    else:
        return key not in dict_two
