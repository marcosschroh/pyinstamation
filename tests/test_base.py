import unittest
from unittest.mock import patch
from pyinstamation.scrapper.base import BaseScrapper
from pyinstamation.scrapper import instagram_const
from pyinstamation import CONFIG
from pyinstamation.config import load_config
from tests import get_free_port, start_mock_server
import time


SLEEP = 1
MOCK_HOSTNAME = 'http://localhost:{port}/'


class BaseScrapperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_config(filepath='test.config.yaml')
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def setUp(self):
        self.base = BaseScrapper()
        self.base.open_browser()
        instagram_const.HOSTNAME = MOCK_HOSTNAME.format(port=self.mock_server_port)
        CONFIG.update({'hide_browser': False})

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

    def test_get_page(self):
        self.base.get_page(instagram_const.HOSTNAME + 'users')
        print(instagram_const.HOSTNAME)
        print(self.base.page_source)
        # time.sleep(20)
        assert True is True
