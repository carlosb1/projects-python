import unittest
from app.proxy_service import ProxyService
# FIXME it is necessary the second test?


class TestProxyService(unittest.TestCase):
    def test_should_not_return_list_when_it_does_not_have_available(self):
        service = ProxyService()
        self.assertTrue(len(service.get_available_proxies([])) == 0)

    def test_should_not_return_list_when_it__has_available(self):
        service = ProxyService()
        self.assertEquals(service.get_available_proxies(['1.1.1.1']), ['1.1.1.1'])
