import unittest
from lwutils.domain_helper import strip_website_hostname


class TestEarlyReductionMethods(unittest.TestCase):
    def test_reduce_hostname(self):
        message = {"httpHost": "dude.google.com"}
        strip_website_hostname(message)

        assert message["httpHost"] == "google.com"

    def test_reduce_hostname_no_reduction_possible(self):
        message = {"httpHost": "google.com"}
        strip_website_hostname(message)

        assert message["httpHost"] == "google.com"
