import os

import imp


def load_config_from_env_file(file):
    config_ret = {}

    filename = os.path.join(os.environ.get(file))
    d = imp.new_module('config')
    d.__file__ = filename
    with open(filename) as config_file:
        exec(compile(config_file.read(), filename, 'exec'), d.__dict__)

    for key in dir(d):
        if key.isupper():
            config_ret[key] = getattr(d, key)
    return config_ret
