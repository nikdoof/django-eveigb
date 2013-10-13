from django.test import TestCase
from mock import Mock

from .middleware import IGBMiddleware


class IGBMiddlewareTest(TestCase):
    """ Test the IGB Middleware """

    def setUp(self):
        self.im = IGBMiddleware()

    def request_factory(self, meta=None):
        rq = Mock(path="/")
        rq.method = 'GET'
        if meta:
            rq.META = meta
        return rq

    def test_invalid_browser_igb(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, False)
        self.assertEqual(request.is_igb_trusted, False)

    def test_invalid_browser_igb_fake_trust(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
            'HTTP_EVE_TRUSTED': 'Yes',
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, False)
        self.assertEqual(request.is_igb_trusted, False)

    def test_valid_igb_no_trust(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0 EVE-IGB',
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, True)
        self.assertEqual(request.is_igb_trusted, False)

    def test_valid_igb_trust(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0 EVE-IGB',
            'HTTP_EVE_TRUSTED': 'Yes',
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, True)
        self.assertEqual(request.is_igb_trusted, True)