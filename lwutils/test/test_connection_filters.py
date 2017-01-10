import unittest
from lwutils.connection_filters import filter_items, filter_items_with_users, is_public_ip, \
    filter_no_data_and_local_ip, filter_no_data_and_local_ip_with_users, filter_items_without_source_hostname, \
    filter_items_with_ports, filter_items_with_users_for_httpHost_or_tag, filter_items_for_httpHost_or_tag


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
        assert not filter_no_data_and_local_ip_with_users(item_without_username)

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

        assert filter_items_with_users_for_httpHost_or_tag(item_with_username_httpHost_no_tag)
        assert filter_items_with_users_for_httpHost_or_tag(item_with_username_no_httpHost_tag)
        assert not filter_items_with_users_for_httpHost_or_tag(item_without_username_but_httpHost)
        assert not filter_items_with_users_for_httpHost_or_tag(item_without_username_but_tag)
        assert not filter_items_with_users_for_httpHost_or_tag(item_without_username_but_tag_and_httpHost)

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
        assert filter_items_for_httpHost_or_tag(item_with_username_httpHost_no_tag)
        assert filter_items_for_httpHost_or_tag(item_with_username_no_httpHost_tag)
        assert filter_items_for_httpHost_or_tag(item_without_username_but_httpHost)
        assert filter_items_for_httpHost_or_tag(item_without_username_but_tag)
        assert not filter_items_for_httpHost_or_tag(item_without_username_no_tag_and_no_httpHost)

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

        assert filter_items_without_source_hostname(item_one_with_source_hostname)
        assert not filter_items_without_source_hostname(item_one_with_no_source_hostname_attribute)
        assert not filter_items_without_source_hostname(item_one_with_no_source_hostname_value)
        assert not filter_items_without_source_hostname(item_one_with_unknown_source_hostname)

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
