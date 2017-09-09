import os
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
        CONFIG.update({'hide_browser': True})
        self.username = CONFIG['username']
        self.password = CONFIG['password']
        self.user_to_follow = 'angie_924'
        self.post_like = 'p%2FBYdLVnQAdfz'

        # patch time.sleep
        # self.patcher = patch('time.sleep')
        # r = self.patcher.start()
        # r.return_value = None
        # self.addCleanup(self.patcher.stop)

        # init scrapper
        self.scrapper = InstaScrapper()
        self.scrapper.open_browser()

    def tearDown(self):
        self.scrapper.close_browser()

    def test_login(self):
        logged = self.scrapper.login(self.username, self.password)
        self.assertTrue(logged)

    def test_logout(self):
        self.scrapper.login(self.username, self.password)
        self.scrapper.logout()
        self.assertIsNone(self.scrapper.browser)

    def test_get_user_info(self):
        self.scrapper.login(self.username, self.password)
        data = self.scrapper.get_user_info(self.username)
        self.scrapper.close_browser()
        self.assertIn('total_followers', data)

    def test_get_user_info_in_post_page(self):
        self.scrapper.login(self.username, self.password)
        data = self.scrapper.get_user_info_in_post_page(self.username)
        self.assertIn('total_followers', data)

    def test_get_user_page(self):
        self.scrapper.get_user_page(self.user_to_follow)
        element = self.scrapper.find('xpath', const.FOLLOW_UNFOLLOW_BUTTON)
        self.assertEqual(element.tag_name, 'button')

    def test_follow_user(self):
        self.scrapper.login(self.username, self.password)
        self.scrapper.follow_user(self.user_to_follow)
        element = self.scrapper.find('xpath', const.FOLLOW_UNFOLLOW_BUTTON)
        self.assertEqual(element.tag_name, 'button')

    def test_unfollow_user(self):
        self.scrapper.login(self.username, self.password)
        self.scrapper.unfollow_user(self.user_to_follow)
        element = self.scrapper.find('xpath', const.FOLLOW_UNFOLLOW_BUTTON)
        self.assertEqual(element.tag_name, 'button')

    def test_follow_unfollow_process(self):
        self.scrapper.login(self.username, self.password)
        result = self.scrapper._follow_unfollow_process(self.user_to_follow)
        self.assertTrue(result)

    def test_like_unlike_process(self):
        self.scrapper.login(self.username, self.password)
        result = self.scrapper._like_unlike_process(self.post_like)
        self.assertFalse(result)
