import json
from threading import Thread
import requests
import time
from time import sleep
from uuid import uuid4


class ERouterClient:

    def __init__(self, erouter_url):
        self.url = erouter_url
        self.publish_retry_count = 10

    def _poll(self, topic_name, subscription_name, callback):
        while True:
            try:
                response = requests.get("%s/topic/%s/%s/poll" % (self.url, topic_name, subscription_name))
                if response.status_code == 200:
                    message = json.loads(response.text).get("message")
                    if message:
                        message_dict = json.loads(message)
                        del_response = requests.delete(
                            "%s/topic/%s/%s/delete/%s" % (self.url, topic_name, subscription_name, message_dict['id']))
                        if del_response.status_code == 200:
                            callback(message_dict['msg'])
                        continue
                    else:
                        time.sleep(2)
            except Exception as e:
                print 'Error during callback for event %s and subscription %s. Error: %s' % (topic_name, subscription_name, e)

    def subscribe(self, topic_name, subscription_name, callback=None, worker_mode=False):
        if not worker_mode:
            subscription_name += "_" + str(uuid4())  # make subscription name unique for scaling
        requests.post("%s/topic/%s/%s/subscribe" % (self.url, topic_name, subscription_name))
        if callback:
            t = Thread(target=self._poll, args=(topic_name, subscription_name, callback,))
            t.daemon = True
            t.start()

    def publish(self, topic_name, message, retry=0):
        try:
            requests.put("%s/topic/%s/publish" % (self.url, topic_name), data=message)
        except Exception as e:
            if retry < self.publish_retry_count:
                sleep(0.1)
                self.publish(topic_name, message, retry=retry + 1)
            else:
                raise e

    def create(self, topic_name):
        requests.put("%s/topic/%s/create" % (self.url, topic_name))
