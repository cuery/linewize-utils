import logging
import collections
from datetime import datetime
import json


class Auditable(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key in self.store:
            self.store[key] += '; ' + str(value)
        else:
            self.store[key] = str(value)

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return repr(self.store)


class ApiAuditor(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.level = {'debug': self.log.debug,
                      'info': self.log.info,
                      'warn': self.log.warn,
                      'error': self.log.error}

    def write(self, auditable, level='info'):
        auditable['timestamp'] = datetime.now().isoformat()
        self.level[level](json.dumps(dict(auditable)))

    def auditable(self, *args, **kwargs):
        return Auditable(*args, **kwargs)
