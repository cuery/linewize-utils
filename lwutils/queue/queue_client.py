from lwutils.queue.clients.aws_queue_client import AWSQueueClient
from lwutils.queue.clients.local_queue_client import LocalQueueClient


class QueueClient(object):

    def factory(config):
        if config.get('QUEUE_PROVIDER') == "AWS":
            return AWSQueueClient(config)
        if config.get('QUEUE_PROVIDER') == "LOCAL":
            return LocalQueueClient(config)
        assert 0, "Unknown Queue provider: " + config.get('QUEUE_PROVIDER', "not configured")
    factory = staticmethod(factory)
