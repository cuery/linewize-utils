from lwutils.mongo_queue import MongoQueue
import time


class LocalQueueClient(object):

    def __init__(self, config):
        self.config = config
        self.queue_client = MongoQueue(self.config)

    def get_queue(self, queue_name):
        queue = LocalQueue(self.queue_client, queue_name)
        return queue


class LocalQueue(object):

    def __init__(self, queue_client, local_queue):
        self.queue_client = queue_client
        self.local_queue = local_queue

    def send_message(self, message_body):
        self.queue_client.add(self.local_queue, message_body)

    def receive_messages(self, max_number_of_messages, wait_time_seconds):
        msgs = []
        msg = self.queue_client.get(self.local_queue)
        # mongo_queue support only single message retrieval atm
        if msg:
            msgs.append(LocalMessage(self.queue_client, self.local_queue, msg))
        else:
            time.sleep(1)  # so we don't run wild, mongo_queue doesn't support wait_time atm
        return msgs


class LocalMessage(object):

    def __init__(self, queue_client, local_queue, msg):
        self.queue_client = queue_client
        self.local_queue = local_queue
        self.msg = msg

    def get_body(self):
        return self.msg['msg']

    def delete(self):
        self.queue_client.delete(self.local_queue, self.msg['id'])
