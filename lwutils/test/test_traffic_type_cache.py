import unittest
import mock
import json
import time
from lwutils.traffic_type_cache import TrafficTypeCache


class Response(object):

    def __init__(self, text):
        self.text = text


class TrafficTypeCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.appindex_response = Response(json.dumps({
            "signatures": [
                {
                    "description": "Gaming",
                    "id": "sphirewall.application.gaming",
                    "is_category": True,
                    "name": "Gaming"
                },
                {
                    "description": "Offensive",
                    "id": "sphirewall.application.offensive",
                    "is_category": True,
                    "name": "Offensive"
                },
                {
                    "category": "sphirewall.application.offensive",
                    "criteria": [
                        [
                            {
                                "conditions": {
                                    "source_url": "http://mirror.sphirewall.net/app_db/blocklists/squid-porn.sphirewall"
                                },
                                "negate": False,
                                "type": "application.http.hostname"
                            }
                        ]
                    ],
                    "description": "This signature matches access to the Pornographic Content",
                    "id": "sphirewall.application.porn",
                    "name": "Pornography"
                },
                {
                    "category": "sphirewall.application.gaming",
                    "criteria": [
                        [
                            {
                                "conditions": [
                                    25565
                                ],
                                "negate": False,
                                "type": "destination.transport.port"
                            }
                        ]
                    ],
                    "description": "This signature matches access to Minecraft traffic",
                    "id": "sphirewall.minecraft",
                    "name": "Minecraft"
                }
            ]
        }))

    @mock.patch('lwutils.traffic_type_cache.requests')
    def test_get_all_signatures(self, requests):
        requests.get.return_value = self.appindex_response
        expected = {}
        expected['sphirewall.application.porn'] = {
            "category": "sphirewall.application.offensive",
            "criteria": [
                        [
                            {
                                "conditions": {
                                    "source_url": "http://mirror.sphirewall.net/app_db/blocklists/squid-porn.sphirewall"
                                },
                                "negate": False,
                                "type": "application.http.hostname"
                            }
                        ]
            ],
            "description": "This signature matches access to the Pornographic Content",
            "id": "sphirewall.application.porn",
            "name": "Pornography"
        }
        expected['sphirewall.minecraft'] = {
            "category": "sphirewall.application.gaming",
            "criteria": [
                        [
                            {
                                "conditions": [
                                    25565
                                ],
                                "negate": False,
                                "type": "destination.transport.port"
                            }
                        ]
            ],
            "description": "This signature matches access to Minecraft traffic",
            "id": "sphirewall.minecraft",
            "name": "Minecraft"
        }

        expected['sphirewall.application.gaming'] =  {u'is_category': True, u'id': u'sphirewall.application.gaming', u'description': u'Gaming', u'name': u'Gaming'}
        expected['sphirewall.application.offensive'] = {u'is_category': True, u'id': u'sphirewall.application.offensive', u'description': u'Offensive', u'name': u'Offensive'}
        cache = TrafficTypeCache('myurl', "fingerprint_url")

        self.assertEqual(expected, cache.get_all_signatures())

    @mock.patch('lwutils.traffic_type_cache.requests')
    def test_get_signature(self, requests):
        requests.get.return_value = self.appindex_response
        expected = {
            "category": "sphirewall.application.gaming",
            "criteria": [
                        [
                            {
                                "conditions": [
                                    25565
                                ],
                                "negate": False,
                                "type": "destination.transport.port"
                            }
                        ]
            ],
            "description": "This signature matches access to Minecraft traffic",
            "id": "sphirewall.minecraft",
            "name": "Minecraft"
        }

        cache = TrafficTypeCache('myurl', "fingerprint_url")

        self.assertEqual(expected, cache.get_signature('sphirewall.minecraft'))

    @mock.patch('lwutils.traffic_type_cache.requests')
    def test_get_signature_unknown(self, requests):
        requests.get.return_value = self.appindex_response

        cache = TrafficTypeCache('myurl', "fingerprint_url")

        self.assertEqual(None, cache.get_signature('sphirewall.unknown'))

    @mock.patch('lwutils.traffic_type_cache.requests')
    def test__cache_expired(self, requests):
        requests.get.return_value = self.appindex_response
        cache = TrafficTypeCache('myurl', "fingerprint_url" ,expiry=2)

        self.assertTrue(cache._cache_expired())
        cache.last_update = time.time()
        self.assertFalse(cache._cache_expired())
        cache.last_update = time.time() - 3
        self.assertTrue(cache._cache_expired())
