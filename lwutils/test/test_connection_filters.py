import unittest
from lwutils.connection_filters import filter_items, filter_items_with_users, is_public_ip, \
    filter_no_data_and_local_ip, filter_no_data_and_local_ip_with_users, filter_items_without_source_hostname, \
    filter_items_with_ports, filter_items_with_users_for_httpHost_or_tag, filter_items_for_httpHost_or_tag, \
    filter_items_with_category, filter_items_with_search_query, filter_item_with_video_views


class TestUpdateAnalyticsFilter(unittest.TestCase):

    def test_filter_zero_byte(self):
        item_upload_download = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_upload = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_download = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 0,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_no_upload_download = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 0,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }

        assert filter_items(item_upload_download)
        assert filter_items(item_upload)
        assert filter_items(item_download)
        assert not filter_items(item_no_upload_download)
        assert filter_no_data_and_local_ip(item_upload_download)
        assert filter_no_data_and_local_ip(item_upload)
        assert filter_no_data_and_local_ip(item_download)
        assert not filter_no_data_and_local_ip(item_no_upload_download)

    def test_filter_without_username(self):
        item_with_username = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_without_username = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': ''
        }

        assert filter_items_with_users(item_with_username)
        assert not filter_items_with_users(item_without_username)
        assert filter_no_data_and_local_ip_with_users(item_with_username)
        assert not filter_no_data_and_local_ip_with_users(
            item_without_username)

    def test_filter_items_with_users_for_httpHost_or_tag(self):
        item_with_username_httpHost_no_tag = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'tag': ''
        }

        item_with_username_no_httpHost_tag = {
            'httpHost': '',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'tag': 'loog_a_tag'
        }

        item_without_username_but_httpHost = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': '',
            'tag': ''
        }

        item_without_username_but_tag = {
            'httpHost': '',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': '',
            'tag': 'look_a_tag'
        }

        item_without_username_but_tag_and_httpHost = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': '',
            'tag': 'look_a_tag'
        }

        assert filter_items_with_users_for_httpHost_or_tag(
            item_with_username_httpHost_no_tag)
        assert filter_items_with_users_for_httpHost_or_tag(
            item_with_username_no_httpHost_tag)
        assert not filter_items_with_users_for_httpHost_or_tag(
            item_without_username_but_httpHost)
        assert not filter_items_with_users_for_httpHost_or_tag(
            item_without_username_but_tag)
        assert not filter_items_with_users_for_httpHost_or_tag(
            item_without_username_but_tag_and_httpHost)

    def test_filter_items_for_httpHost_or_tag(self):
        item_with_username_httpHost_no_tag = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'tag': ''
        }

        item_with_username_no_httpHost_tag = {
            'httpHost': '',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'tag': 'loog_a_tag'
        }

        item_without_username_but_httpHost = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': '',
            'tag': ''
        }

        item_without_username_but_tag = {
            'httpHost': '',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': '',
            'tag': 'look_a_tag'
        }

        item_without_username_no_tag_and_no_httpHost = {
            'httpHost': '',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': '',
            'tag': ''
        }

        filter_items_for_httpHost_or_tag
        assert filter_items_for_httpHost_or_tag(
            item_with_username_httpHost_no_tag)
        assert filter_items_for_httpHost_or_tag(
            item_with_username_no_httpHost_tag)
        assert filter_items_for_httpHost_or_tag(
            item_without_username_but_httpHost)
        assert filter_items_for_httpHost_or_tag(item_without_username_but_tag)
        assert not filter_items_for_httpHost_or_tag(
            item_without_username_no_tag_and_no_httpHost)

    def test_filter_invalid_website(self):
        item_with_valid_website = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_with_another_valid_website = {
            'httpHost': 'pcschool.cbhs',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_with_invalid_website = {
            'httpHost': 'garble',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': ''
        }
        item_with_no_website = {
            'httpHost': '',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 0,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': ''
        }

        assert filter_items(item_with_valid_website)
        assert filter_items(item_with_another_valid_website)
        assert not filter_items(item_with_invalid_website)
        assert not filter_items(item_with_no_website)
        assert filter_no_data_and_local_ip(item_with_valid_website)
        assert filter_no_data_and_local_ip(item_with_another_valid_website)
        assert filter_no_data_and_local_ip(item_with_invalid_website)
        assert filter_no_data_and_local_ip(item_with_no_website)

    def test_filter_external_ips(self):
        item_one_with_local_ip = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_two_with_local_ip = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '172.18.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_three_with_local_ip = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '192.168.4.11',
            'time': '1386810101',
            'user': 'da_user'
        }
        item_with_external_ip = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '54.21.44.44',
            'time': '1386810101',
            'user': 'da_user'
        }

        assert filter_items(item_one_with_local_ip)
        assert filter_items(item_two_with_local_ip)
        assert filter_items(item_three_with_local_ip)
        assert not filter_items(item_with_external_ip)
        assert filter_no_data_and_local_ip(item_one_with_local_ip)
        assert filter_no_data_and_local_ip(item_two_with_local_ip)
        assert filter_no_data_and_local_ip(item_three_with_local_ip)
        assert not filter_no_data_and_local_ip(item_with_external_ip)

    def test_is_public_ip(self):
        self.assertTrue(is_public_ip('123.14.65.32'))
        self.assertFalse(is_public_ip(''))
        self.assertFalse(is_public_ip('afdkjhasd'))
        self.assertFalse(is_public_ip('123.14.65'))
        self.assertFalse(is_public_ip('123.14'))
        self.assertFalse(is_public_ip('123'))
        self.assertFalse(is_public_ip('10.1.23.34'))
        self.assertFalse(is_public_ip('172.24.1.66'))
        self.assertFalse(is_public_ip('192.168.255.255'))

    def test_filter_items_without_source_hostname(self):
        item_one_with_source_hostname = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'sourceHostname': 'localhost'
        }

        item_one_with_no_source_hostname_attribute = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }

        item_one_with_no_source_hostname_value = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'sourceHostname': ''
        }

        item_one_with_unknown_source_hostname = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'sourceHostname': 'unknown'
        }

        assert filter_items_without_source_hostname(
            item_one_with_source_hostname)
        assert not filter_items_without_source_hostname(
            item_one_with_no_source_hostname_attribute)
        assert not filter_items_without_source_hostname(
            item_one_with_no_source_hostname_value)
        assert not filter_items_without_source_hostname(
            item_one_with_unknown_source_hostname)

    def test_filter_ports(self):
        item_one = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'sourceHostname': 'localhost'
        }

        item_two = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 43243,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user'
        }
        assert filter_items_with_ports(item_one)
        assert not filter_items_with_ports(item_two)

    def test_filter_category(self):
        item_no_categoryId = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'sourceHostname': 'localhost'
        }

        item_empty_categoryId = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 43243,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'categoryId': ''
        }

        item_with_categoryId = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 43243,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'categoryId': 'sphirewall.application.internetandtelecom'
        }

        assert not filter_items_with_category(item_no_categoryId)
        assert not filter_items_with_category(item_empty_categoryId)
        assert filter_items_with_category(item_with_categoryId)

    def test_filter_items_with_search_query(self):
        item_one = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': []
        }
        item_two = {
            'httpHost': 'www.bing.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["foo bar"]
        }
        item_bing_search = {
            'httpHost': 'www.bing.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["/search?q=how+to+make+bomb&form=EDGEAR&qs=OS&cvid=ae3743f5cc154c6b89c09a9209176260&cc=AU&setlang=en-US"]
        }
        item_google_search = {
            'httpHost': 'www.google.co.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["/search?dcr=0&source=hp&ei=0BVdWryCPMiu8QWy3YrwBQ&q=foo&oq=foo&gs_l=psy-ab.3..0l2j0i131k1j0l2j0i131k1l3j0l2.3881.4180.0.4468.4.3.0.0.0.0.215.215.2-1.1.0....0...1c.1.64.psy-ab..3.1.214.0...0.rLeXT0Jqqrk"]
        }
        item_yahoo_search = {
            'httpHost': 'nz.search.yahoo.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["/search?p=adventure+bike&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8"]
        }
        item_duck_duck_go_search = {
            'httpHost': 'duckduckgo.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["/?q=hard+rock+music&t=hf&ia=audio"]
        }
        item_bing = {
            "sourceIp": "10.61.164.13",
            "destIp": "",
            "sourcePort": 0,
            "destPort": 80,
            "time": 1517372173,
            "packets": 0,
            "lifetime": 0,
            "upload": 1106,
            "download": 47638,
            "protocol": 6,
            "final_connection_object": True,
            "hwAddress": "dc:a9:04:7e:bb:79",
            "user": "cn=darel lasrado,ou=staff,dc=bxh01,dc=prd,dc=familyzone,dc=com",
            "httpHost": "www.bing.com",
            "tag": "",
            "subCategoryId": "-",
            "categoryId": "CT-Search_Engines_And_Portals",
            "http_request_uris": [
                "GET /search?q=bingo+australia\u0026qs=n\u0026form=QBRE\u0026sp=-1\u0026pq=bingo+australia\u0026sc=8-15\u0026sk=\u0026cvid=94E3D165B94243A7AB8DA1AB06332515"
            ],
            "app_filtering_denied": False,
            "verdict_filter_rule": "OK",
            "cache_state": "MISS"
        }
        item_michaesearch = {
            "app_filtering_denied": False,
            "categoryId": "",
            "contenttype": "application/json; charset=UTF-8",
            "destIp": "216.58.203.100",
            "destPort": 443,
            "download": 720,
            "final_connection_object": True,
            "fingerprint": "",
            "geoip_destination": "US",
            "geoip_source": "",
            "httpHost": "www.google.com",
            "http_request_uris": ["GET /search?client=psy-ab&hl=en-NZ&gs_rn=64&gs_ri=psy-ab&pq=sex&cp=4&gs_id=v&q=test&xhr=t HTTP/1.1"],
            "hwAddress": "-",
            "inputDev": "",
            "lifetime": 0,
            "noise": True,
            "outputDev": "",
            "packets": 3,
            "protocol": 6,
            "referer": "https://www.google.com/",
            "sourceHostname": "",
            "sourceIp": "192.168.179.21",
            "sourcePort": 61770,
            "subCategoryId": "",
            "tag": "",
            "time": 1517435680,
            "upload": 0,
            "user": "",
            "useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        item_michaesearch_xhr = {
            "app_filtering_denied": False,
            "categoryId": "",
            "contenttype": "application/json; charset=UTF-8",
            "destIp": "216.58.203.100",
            "destPort": 443,
            "download": 720,
            "final_connection_object": True,
            "fingerprint": "",
            "geoip_destination": "US",
            "geoip_source": "",
            "httpHost": "www.google.com",
            "http_request_uris": ["GET /complete/search?client=psy-ab&hl=en-NZ&gs_rn=64&gs_ri=psy-ab&pq=sex&cp=4&gs_id=v&q=test&xhr=t HTTP/1.1"],
            "hwAddress": "-",
            "inputDev": "",
            "lifetime": 0,
            "noise": True,
            "outputDev": "",
            "packets": 3,
            "protocol": 6,
            "referer": "https://www.google.com/",
            "sourceHostname": "",
            "sourceIp": "192.168.179.21",
            "sourcePort": 61770,
            "subCategoryId": "",
            "tag": "",
            "time": 1517435680,
            "upload": 0,
            "user": "",
            "useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        assert not filter_items_with_search_query(item_one)
        assert not filter_items_with_search_query(item_two)
        assert filter_items_with_search_query(item_bing_search)
        assert filter_items_with_search_query(item_bing)
        assert filter_items_with_search_query(item_google_search)
        assert filter_items_with_search_query(item_yahoo_search)
        assert filter_items_with_search_query(item_duck_duck_go_search)
        assert filter_items_with_search_query(item_michaesearch)
        assert not filter_items_with_search_query(item_michaesearch_xhr)


    def test_filter_item_with_video_views(self):
        item_one = {
            'httpHost': 'pcschool.cbhs.school.nz',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': []
        }
        item_two = {
            'httpHost': 'www.bing.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["foo bar"]
        }
        item_youtube_search = {
            'httpHost': 'www.youtube.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["GET /results?search_query=hard+rock"]
        }
        item_youtube_video_view = {
            'httpHost': 'www.youtube.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["GET /watch?v=hhdDY0y-j5g"]
        }
        item_youtube_video_view_time_select = {
            'httpHost': 'www.youtube.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["GET /watch?v=hhdDY0y-j5g&feature=youtu.be&t=115"]
        }
        item_youtube_video_view_playlist = {
            'httpHost': 'www.youtube.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["GET /watch?v=Ypkv0HeUvTc&list=PLf7fnw8RkLVda0FdsKI1Eddf0NQOLwuxe"]
        }
        item_youtube_video_view_playlist_next_video = {
            'httpHost': 'www.youtube.com',
            'hwAddress': '98:0c:82:5d:df:6a',
            'destPort': 80,
            'upload': 654925,
            'download': 4203181,
            'sourceIp': '10.103.1.36',
            'time': '1386810101',
            'user': 'da_user',
            'http_request_uris': ["GET /watch?v=QUvVdTlA23w&list=PLf7fnw8RkLVda0FdsKI1Eddf0NQOLwuxe&index=2"]
        }
        assert not filter_item_with_video_views(item_one)
        assert not filter_item_with_video_views(item_two)
        assert not filter_item_with_video_views(item_youtube_search)
        assert filter_item_with_video_views(item_youtube_video_view)
        assert filter_item_with_video_views(item_youtube_video_view_time_select)
        assert filter_item_with_video_views(item_youtube_video_view_playlist)
        assert filter_item_with_video_views(item_youtube_video_view_playlist_next_video)