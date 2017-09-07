import os
import unittest
from unittest.mock import patch

from pyinstamation import CONFIG
from pyinstamation.config import load_config
from pyinstamation.scrapper.base import BaseScrapper
from pyinstamation.scrapper import instagram_const as const
from tests import get_free_port, start_mock_server, MOCK_HOSTNAME


SLEEP = 1


class BaseScrapperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_config(filepath='test.config.yaml')
        mock_server_port = get_free_port()
        start_mock_server(mock_server_port)
        const.HOSTNAME = MOCK_HOSTNAME.format(port=mock_server_port)

    def setUp(self):
        CONFIG.update({'hide_browser': True})
        self.base = BaseScrapper()
        self.base.open_browser()

    def tearDown(self):
        if self.base.browser is not None:
            self.base.close_browser()

    def test_open_mobile_browser(self):
        self.base.close_browser()
        self.base.open_browser()
        self.assertIsNotNone(self.base.browser)

    def test_open_mobile_browser_hidden(self):
        CONFIG.update({'hide_browser': True})
        self.base.close_browser()
        self.base.open_browser()
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

    @patch('time.sleep', return_value=None)
    def test_get_page(self, time_sleep):
        self.base.get_page('accounts/login')
        self.assertIsInstance(self.base.page_source, str)

    @patch('time.sleep', return_value=None)
    def test_find(self, time_sleep):
        self.base.get_page('accounts/login')
        username_input = self.base.find('xpath', const.LOGIN_INPUT_USERNAME)
        self.assertEqual(username_input.tag_name, 'input')

    def test_random_seconds(self):
        sec = self.base.random_seconds()
        self.assertIsInstance(sec, int)
        self.assertIn(sec, range(1, 11))

    def test_to_mobile_dimension(self):
        CONFIG.update({'hide_browser': True})
        self.base.to_mobile_dimension()
        size = self.base.browser.get_window_size()
        self.assertTrue(size.get('width') >= self.base.MOBILE_WIDTH)
        self.assertTrue(size.get('height') >= self.base.MOBILE_HEIGTH)
