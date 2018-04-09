import json
import time
import urllib
from uuid import uuid4
from tornado.httpclient import AsyncHTTPClient
from tornado import gen


class AsyncERouterClient:

    def __init__(self, erouter_url):
        self.url = erouter_url
        self.publish_retry_count = 10

    @gen.coroutine
    def fetch_coroutine(self, url, **kwargs):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url, **kwargs)
        raise gen.Return(response)   

    @gen.coroutine
    def _poll(self, topic_name, subscription_name, callback):
        while True:
            try:
                response = yield self.fetch_coroutine("%s/topic/%s/%s/poll" % (self.url, topic_name, subscription_name))
                if response.code == 200:
                    message = json.loads(response.body).get("message")
                    if message:
                        message_dict = json.loads(message)
                        del_response = yield self.fetch_coroutine(
                            "%s/topic/%s/%s/delete/%s" % (self.url, topic_name, subscription_name, message_dict['id']),
                            method="DELETE")
                        if del_response.code == 200:
                            callback(message_dict['msg'])
                        continue
                    else:
                        yield gen.sleep(2)
            except Exception as e:
                print 'Error during call'       
    
    @gen.coroutine
    def subscribe(self, topic_name, subscription_name, callback=None, worker_mode=False):
        if not worker_mode:
            subscription_name += "_" + str(uuid4())  # make subscription name unique for scaling
        response = yield self.fetch_coroutine("%s/topic/%s/%s/subscribe" % (self.url, topic_name, subscription_name), method="POST", body="")
        if response.code == 200 and callback:
            yield self._poll(topic_name, subscription_name, callback)

    @gen.coroutine
    def publish(self, topic_name, message, retry=0):
        try:
            body = urllib.urlencode(message)
            yield self.fetch_coroutine("%s/topic/%s/publish" % (self.url, topic_name), body=body)
        except Exception as e:
            if retry < self.publish_retry_count:
                yield gen.sleep(0.1)
                self.publish(topic_name, message, retry=retry + 1)
            else:
                raise e

    @gen.coroutine
    def create(self, topic_name):
        yield self.fetch_coroutine("%s/topic/%s/create" % (self.url, topic_name), method="PUT")   