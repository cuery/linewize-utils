import unittest
import mock
from lwutils.erouter_client import ERouterClient


class ERouterClientTestCase(unittest.TestCase):

    @mock.patch('lwutils.erouter_client.requests')
    def test_publish(self, requests):
        client = ERouterClient("myurl.com")
        try:
            client.publish('mytopic', 'mymessage')
        except Exception as e:
            self.fail(e)
        requests.put.assert_called_with("myurl.com/topic/mytopic/publish", data='mymessage')

    @mock.patch('lwutils.erouter_client.requests')
    def test_publish_retry(self, requests):
        returns = [Exception('boom'), 'response']
        requests.put.side_effect = returns
        client = ERouterClient("myurl.com")
        try:
            client.publish('mytopic', 'mymessage')
        except Exception:
            self.fail()
        requests.put.assert_called_with("myurl.com/topic/mytopic/publish", data='mymessage')

    @mock.patch('lwutils.erouter_client.requests')
    def test_publish_retry_exception(self, requests):
        requests.put.side_effect = Exception('boom')
        client = ERouterClient("myurl.com")
        with self.assertRaises(Exception):
            client.publish('mytopic', 'mymessage')
