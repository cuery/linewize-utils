from lwutils.queue.clients.aws_queue_client import AWSQueueClient
from lwutils.queue.clients.local_queue_client import LocalQueueClient
from lwutils.queue.clients.inmemory_queue_client import InMemoryQueueClient


class QueueClient(object):

    def factory(config):
        if config.get('QUEUE_PROVIDER') == "AWS":
            return AWSQueueClient(config)
        elif config.get('QUEUE_PROVIDER') == "LOCAL":
            return LocalQueueClient(config)
        elif config.get('QUEUE_PROVIDER') == "INMEMORY":
            return InMemoryQueueClient(config)
        else:
            print "Unknown Queue provider: " + config.get('QUEUE_PROVIDER', "not configured")
    factory = staticmethod(factory)
