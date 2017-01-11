import Queue


class InMemoryQueueClient(object):
    """
    Use only for UNIT TESTS! not fully implemented in regards to message persistence
    """

    def __init__(self, config):
        self.config = config
        self.queues = {}

    def get_queue(self, queue_name):
        queue = InMemoryQueue(self.queues, queue_name)
        return queue


class InMemoryQueue(object):

    def __init__(self, queues, queue_name):
        self.queues = queues
        self.queue_name = queue_name
        if queue_name not in self.queues:
            self.queues[queue_name] = Queue.Queue()

    def send_message(self, message_body):
        self.queues[self.queue_name].put(message_body)

    def receive_messages(self, max_number_of_messages, wait_time_seconds):
        msgs = []
        try:
            # Queue support only single message retrieval
            msgs.append(InMemoryMessage(self.queues[self.queue_name].get(timeout=wait_time_seconds)))
        except Queue.Empty:
            pass
        return msgs


class InMemoryMessage(object):

    def __init__(self, msg):
        self.msg = msg

    def get_body(self):
        return self.msg

    def delete(self):
        pass  # see comment on top of InMemoryQueueClient class
