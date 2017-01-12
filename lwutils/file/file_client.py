from lwutils.file.clients.aws_file_client import AWSFileClient
from lwutils.file.clients.local_file_client import LocalFileClient


class FileClient(object):

    def factory(config):
        if config.get('FILE_PROVIDER') == "AWS":
            return AWSFileClient(config)
        elif config.get('FILE_PROVIDER') == "LOCAL":
            return LocalFileClient(config)
        else:
            print "Unknown File provider: " + config.get('FILE_PROVIDER', "not configured")
    factory = staticmethod(factory)
