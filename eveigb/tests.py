from django.test import TestCase
from mock import Mock

from .middleware import IGBMiddleware


class IGBMiddlewareTest(TestCase):
    """ Test the IGB Middleware """

    def setUp(self):
        self.im = IGBMiddleware()
        self.igb_user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0 EVE-IGB'
        self.non_igb_user_agent = 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'

    def request_factory(self, meta=None):
        rq = Mock(path="/")
        rq.method = 'GET'
        if meta:
            rq.META = meta
        return rq

    def test_invalid_browser_igb(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': self.non_igb_user_agent
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, False)
        self.assertEqual(request.is_igb_trusted, False)

    def test_invalid_browser_igb_fake_trust(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': self.non_igb_user_agent,
            'HTTP_EVE_TRUSTED': 'Yes',
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, False)
        self.assertEqual(request.is_igb_trusted, False)

    def test_valid_igb_no_trust(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': self.igb_user_agent
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, True)
        self.assertEqual(request.is_igb_trusted, False)

    def test_valid_igb_trust(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': self.igb_user_agent,
            'HTTP_EVE_TRUSTED': 'Yes',
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, True)
        self.assertEqual(request.is_igb_trusted, True)

    def test_valid_igb_trust_extra_headers(self):
        request = self.request_factory({
            'HTTP_USER_AGENT': self.igb_user_agent,
            'HTTP_EVE_TRUSTED': 'Yes',
            'HTTP_EVE_CHARID': '12345678',
            'HTTP_EVE_CORPNAME': 'Llama Inc.',
            'HTTP_EVE_CORPID': '3456789',
            'HTTP_EVE_ALLIANCENAME': 'Fandab',
        })
        self.im.process_request(request)
        self.assertEqual(request.is_igb, True)
        self.assertEqual(request.is_igb_trusted, True)
        self.assertEquals(request.eve_charid, '12345678')
        self.assertEquals(request.eve_corpname, 'Llama Inc.')
        self.assertEquals(request.eve_corpid, '3456789')
        self.assertEquals(request.eve_alliancename, 'Fandab')

    def test_valid_igb_trust_invalid_secure(self):
        with self.settings(EVEIGB_SECURE_HEADERS=True):
            request = self.request_factory({
                'HTTP_USER_AGENT': self.igb_user_agent,
                'HTTP_EVE_TRUSTED': 'Yes',
                'HTTP_EVE_CHARID': '12345678',
                'HTTP_EVE_CORPNAME': 'Llama Inc.',
                'HTTP_EVE_CORPID': '3456789',
                'HTTP_EVE_ALLIANCENAME': 'Fandab',
            })
            self.im.process_request(request)
            self.assertEqual(request.is_igb, False)
            self.assertEqual(request.is_igb_trusted, False)

    def test_valid_igb_trust_secure(self):
        with self.settings(EVEIGB_SECURE_HEADERS=True):
            request = self.request_factory({
                'HTTP_USER_AGENT': self.igb_user_agent,
                'HTTP_EVE_TRUSTED': 'Yes',
                'HTTP_EVE_CHARNAME': 'Bob McBobbington',
                'HTTP_EVE_CHARID': '123456789',
                'HTTP_EVE_CORPNAME': 'Bob Inc.',
                'HTTP_EVE_CORPID': '456789',
                'HTTP_EVE_REGIONNAME': 'Delve',
                'HTTP_EVE_CONSTELLATIONNAME': 'Somewhere',
                'HTTP_EVE_SOLARSYSTEMNAME': 'NOL',
                'HTTP_EVE_CORPROLE': '0',
                'HTTP_EVE_SHIPNAME': 'Llamageddon',
                'HTTP_EVE_SHIPTYPEID': '12345',
                'HTTP_EVE_SHIPTYPENAME': 'Eeep',
                'HTTP_EVE_SHIPID': '1234435',
                'HTTP_EVE_SOLARSYSTEMID': '1234234',
            })
            self.im.process_request(request)
            self.assertEqual(request.is_igb, True)
            self.assertEqual(request.is_igb_trusted, True)
            self.assertEquals(request.eve_charid, '123456789')
            self.assertEquals(request.eve_corpname, 'Bob Inc.')
            self.assertEquals(request.eve_corpid, '456789')

    def test_valid_igb_trust_secure_invalid_data(self):
        with self.settings(EVEIGB_SECURE_HEADERS=True):
            request = self.request_factory({
                'HTTP_USER_AGENT': self.igb_user_agent,
                'HTTP_EVE_TRUSTED': 'Yes',
                'HTTP_EVE_CHARNAME': 'Bob McBobbington',
                'HTTP_EVE_CHARID': 'xyz',
                'HTTP_EVE_CORPNAME': 'Bob Inc.',
                'HTTP_EVE_CORPID': '456789',
                'HTTP_EVE_REGIONNAME': 'Delve',
                'HTTP_EVE_CONSTELLATIONNAME': 'Somewhere',
                'HTTP_EVE_SOLARSYSTEMNAME': 'NOL',
                'HTTP_EVE_CORPROLE': '0',
                'HTTP_EVE_SHIPNAME': 'Llamageddon',
                'HTTP_EVE_SHIPTYPEID': '12345',
                'HTTP_EVE_SHIPTYPENAME': 'Eeep',
                'HTTP_EVE_SHIPID': '1234435',
                'HTTP_EVE_SOLARSYSTEMID': '1234234',
            })
            self.im.process_request(request)
            self.assertEqual(request.is_igb, False)
            self.assertEqual(request.is_igb_trusted, False)