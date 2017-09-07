import unittest

from unittest.mock import patch
from pyinstamation import CONFIG
from pyinstamation.config import load_config
from pyinstamation.scrapper import InstaScrapper
from pyinstamation.scrapper import instagram_const as const
from tests import get_free_port, start_mock_server, MOCK_HOSTNAME


class BaseScrapperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_config(filepath='test.config.yaml')
        mock_server_port = get_free_port()
        start_mock_server(mock_server_port)
        const.HOSTNAME = MOCK_HOSTNAME.format(port=mock_server_port)

    def setUp(self):
        CONFIG.update({'hide_browser': False})

        # patch time.sleep
        self.patcher = patch('time.sleep')
        r = self.patcher.start()
        r.return_value = None
        self.addCleanup(self.patcher.stop)

        # init scrapper
        self.scrapper = InstaScrapper()
        self.scrapper.open_browser()

    def tearDown(self):
        if self.scrapper.browser is not None:
            self.scrapper.close_browser()

    # @patch('selenium.webdriver.remote.webelement.WebElement.click', return_value=print("Hoooooooooooolis"))
    def test_login(self):
        logged = self.scrapper.login(CONFIG['username'], CONFIG['password'])
        self.assertTrue(logged)
