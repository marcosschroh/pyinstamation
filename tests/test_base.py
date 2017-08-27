import unittest
from unittest.mock import patch
from pyinstamation.scrapper.base import BaseScrapper


SLEEP = 1
URL_TO_GET = 'https://www.instagram.com/'


class MockResponse:
    code = 200
    headers = []

    def read(self):
        return b"{}"

    def close(self):
        pass

    def getheader(self, *args, **kwargs):
        pass


class BaseScrapperTest(unittest.TestCase):

    def setUp(self):
        self.base = BaseScrapper()
        self.base.open_browser()

    def tearDown(self):
        if self.base.browser is not None:
            self.base.close_browser()

    def test_open_mobile_browser(self):
        self.assertIsNotNone(self.base.browser)

    def test_close_browser(self):
        self.base.close_browser()
        self.assertIsNone(self.base.browser)

    def test_wait_sleep_time_none_explicit_false(self):
        with patch('random.randrange', return_value=SLEEP):
            waited = self.base.wait(explicit=False)
            self.assertEqual(waited, SLEEP)

    @patch('time.sleep', return_value=None)
    def test_wait_sleep_time_none_explicit_true(self, time_sleep):
        with patch('random.randrange', return_value=SLEEP):
            waited = self.base.wait(explicit=True)
            self.assertEqual(waited, SLEEP)

    @patch('time.sleep', return_value=None)
    def test_wait_sleep_time_defined(self, time_sleep):
        waited = self.base.wait(sleep_time=SLEEP, explicit=True)
        self.assertEqual(waited, SLEEP)
