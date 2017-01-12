from lwutils.boto3.resource import Resource


class AWSQueueClient(object):

    def __init__(self, config):
        self.config = config
        self.sqs = Resource(self.config).sqs()

    def get_queue(self, queue_name):
        queue = AWSQueue(self.sqs.get_queue_by_name(QueueName=queue_name))
        return queue


class AWSQueue(object):

    def __init__(self, sqs_queue):
        self.sqs_queue = sqs_queue

    def send_message(self, message_body):
        self.sqs_queue.send_message(MessageBody=message_body)

    def receive_messages(self, max_number_of_messages, wait_time_seconds):
        msgs = []
        sqs_msgs = self.sqs_queue.receive_messages(
            MaxNumberOfMessages=max_number_of_messages, WaitTimeSeconds=wait_time_seconds)
        for sqs_msg in sqs_msgs:
            msgs.append(AWSMessage(sqs_msg))
        return msgs


class AWSMessage(object):

    def __init__(self, sqs_msg):
        self.sqs_msg = sqs_msg

    def get_body(self):
        return self.sqs_msg.body

    def delete(self):
        self.sqs_msg.delete()
