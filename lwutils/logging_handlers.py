import logging.handlers as handlers
import os


class DynamicTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):

    def __init__(self, filename, backupCount=0, encoding=None, delay=0, when='h', interval=1, utc=False):
        path_token = filename.split('.')
        new_filename = path_token[0] + '_' + str(os.getpid()) + '.' + path_token[1]
        handlers.TimedRotatingFileHandler.__init__(
            self, filename=new_filename, when=when, interval=interval, backupCount=backupCount, encoding=encoding, delay=delay, utc=utc)
