import time
import logging


class Timer(object):

    """
    usage:
        with Timer() as t:
            filtered_items = handler.filter(items)
        print "=> elasped filter: %s s" % t.secs
    or:
        with Timer(verbose=True):
            domain = self._extract_domain(item['httpHost'])
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self._logger = logging.getLogger(__name__)

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            self._logger('elapsed time: %f ms' % self.msecs)
