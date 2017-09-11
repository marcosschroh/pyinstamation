import os
import unittest
from urllib.parse import urlparse
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

        self.user_to_follow = 'fancyhoustonapartments'
        self.user_to_unfollow = 'celine_legallic'

        self.post_path_no_like = 'BY3rdjrH-cr'
        self.post_link_no_like = 'p/{0}/'.format(self.post_path_no_like)

        self.post_path_liked = 'BY3Bg4THwNi'
        self.post_link_liked = 'p/{0}/'.format(self.post_path_liked)

        self.hastag = 'apartmentdecor'

        self.filepath = os.path.abspath('one_day.jpg')
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

    def test_user_info(self):
        self.scrapper.login(self.username, self.password)
        data = self.scrapper.user_info(self.username)
        self.scrapper.close_browser()
        self.assertIn('total_followers', data)

    def test_user_info_in_post_page(self):
        self.scrapper.login(self.username, self.password)
        data = self.scrapper.user_info_in_post_page(self.username)
        self.assertIn('total_followers', data)

    def test_user_page(self):
        self.scrapper.user_page(self.user_to_follow)
        element = self.scrapper.find('xpath', const.FOLLOW_UNFOLLOW_BUTTON)
        self.assertEqual(element.tag_name, 'button')

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper._validate_follow_click', return_value=True)
    def test_follow_user(self, validate_follow_click_fn):
        result = self.scrapper.follow(self.user_to_follow)
        self.assertTrue(result)

    def test_follow_user_failed(self):
        result = self.scrapper.follow(self.user_to_follow)
        self.assertFalse(result)

    def test_follow_in_followed_user(self):
        follow_succesful = self.scrapper.follow(self.user_to_unfollow)
        self.assertFalse(follow_succesful)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper._validate_follow_click', return_value=True)
    def test_unfollow_user(self, validate_follow_click_fn):
        result = self.scrapper.unfollow(self.user_to_unfollow)
        self.assertTrue(result)

    def test_unfollow_user_fail(self):
        result = self.scrapper.unfollow(self.user_to_unfollow)
        self.assertFalse(result)

    def test_unfollow_in_not_followed_user(self):
        unfollow_succesful = self.scrapper.unfollow(self.user_to_follow)
        self.assertFalse(unfollow_succesful)

    def test_is_liked(self):
        self.scrapper.get_page(self.post_link_liked)
        self.assertTrue(self.scrapper._is_liked)

    def test_not_is_liked(self):
        self.scrapper.get_page(self.post_link_no_like)
        self.assertFalse(self.scrapper._is_liked)

    def test_like(self):
        result = self.scrapper.like(self.post_link_no_like)
        self.assertTrue(result)

    def test_like_fail(self):
        result = self.scrapper.like(self.post_link_liked)
        self.assertFalse(result)

    def test_unlike(self):
        result = self.scrapper.unlike(self.post_link_liked)
        self.assertTrue(result)

    def test_unlike_fail(self):
        result = self.scrapper.unlike(self.post_link_no_like)
        self.assertFalse(result)

    def test_username_in_post_page(self):
        username = self.scrapper.username_in_post_page(self.post_link_liked)
        self.assertEqual(username, 'fancyhoustonapartments')

    @unittest.skip("no way to properly test yet")
    def test_comment(self):
        comment = 'this is a comment'
        result = self.scrapper.comment(self.post_link_liked, comment)
        self.assertTrue(result)

    def test_generate_post_link_by_code(self):
        result = self.scrapper.generate_post_link_by_code(self.post_path_no_like)
        self.assertEqual(result, self.post_link_no_like)

    def test_get_hashtag_page(self):
        self.scrapper.get_hashtag_page(self.hastag)
        self.assertEqual(self.scrapper.current_url.path,
                         '/explore/tags/{0}/'.format(self.hastag))

    def test_get_posts_by_hashtag(self):
        result = self.scrapper.get_posts_by_hashtag(self.hastag)
        self.assertEqual(len(result), 18)

    @unittest.skip("TODO: FIX ERROR")
    def test_upload_picture(self):
        self.scrapper.get_page('/')
        r = self.scrapper.upload_picture(self.filepath, description='not real')
        self.assertTrue(r)
