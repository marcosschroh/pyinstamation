import unittest
from datetime import datetime
from unittest.mock import patch

from pyinstamation.scrapper.insta_scrapper import InstaScrapper
from pyinstamation import config
from pyinstamation.bot import InstaBot, FollowedUser


class BotTestCase(unittest.TestCase):

    def setUp(self):
        config.load_config(filepath='test.config.yaml')
        username = 'username'
        password = 'password'
        self.scrapper = InstaScrapper(hide_browser=True)
        self.bot = InstaBot(self.scrapper, username=username, password=password)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_login(self, login_fn):
        self.bot.login()
        self.assertEqual(self.bot.user_login, True)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.logout', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_logout(self, login_fn, logout_fn):
        self.assertFalse(self.bot.logout())
        self.bot.login()
        self.assertTrue(self.bot.logout())

    @patch('random.uniform', return_value=0.5)
    def test_probability_of_occurrence(self, uniform_fn):
        self.assertTrue(self.bot.probability_of_occurrence(0.6))
        self.assertFalse(self.bot.probability_of_occurrence(0.4))

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_user_info', return_value={
        'total_followers': 100,
        'total_following': 50
    })
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_get_my_profile_info(self, login_fn, get_user_info_fn):
        self.bot.login()
        self.bot.get_my_profile_info()
        self.assertEqual(self.bot.total_followers, 100)
        self.assertEqual(self.bot.total_following, 50)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.upload_picture', return_value=True)
    def test_upload_picture(self, upload_picture_fn):
        self.bot.upload_picture('image_path', 'comment')
        self.assertEqual(self.bot.pictures_uploaded, 1)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.upload_picture', return_value=True)
    def test_upload_multiple_pictures(self, upload_picture_fn):
        images = [
            {
                'comment': '#motivation',
                'datetime': '2017-08-31T13:30:00',
                'path': '/home/User/Pictures/one_day.jpg'
            },
            {
                'comment': '#motivation2',
                'datetime': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                'path': '/home/User/Pictures/two_day.jpg'
            },
            {
                'comment': '#motivation3',
                'datetime': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                'path': '/home/User/Pictures/three_day.jpg'
            },
        ]

        self.bot.upload_multiple_pictures(images)
        self.assertEqual(self.bot.pictures_uploaded, 2)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unfollow_user', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_unfollow_user(self, login_fn, unfollow_user_fn):
        self.bot.login()

        username = 'Foo'
        self.bot.unfollow_user(username)
        self.assertTrue(
            len([u for u in self.bot.users_unfollowed_by_bot if u.username == username])
        )

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unfollow_user', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_unfollow_multiple_users(self, login_fn, unfollow_user_fn):
        self.bot.login()
        users = [
            FollowedUser('Hi', '_'),
            FollowedUser('Chiche', '_')
        ]

        self.bot.unfollow_multiple_users(users)
        unfollow_users = [u.username for u in self.bot.users_unfollowed_by_bot]

        self.assertTrue('Hi' in unfollow_users)
        self.assertTrue('Chiche' in unfollow_users)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_user_info', return_value={
        'total_followers': 100,
        'total_following': 50
    })
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.follow_user', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_follow_user(self, login_fn, follow_user_fn, get_user_info_fn):
        self.assertFalse(self.bot.follow_user(''))
        self.bot.login()

        username = 'Bar'
        self.bot.follow_user(username)
        self.assertTrue(
            len([u for u in self.bot.users_followed_by_bot if u.username == username])
        )

        self.assertFalse(self.bot.follow_user(
            username, conditions_checked=False, min_followers=101))

    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.follow_user', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_follow_multiple_users(self, login_fn, follow_user_fn, should_follow_fn):
        self.bot.login()
        self.bot.follow_multiple_users(['user1', 'user2'])
        self.assertEqual(self.bot.total_user_followed_by_bot, 2)

    @patch('pyinstamation.bot.InstaBot.probability_of_occurrence', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_user_info', return_value={
        'total_followers': 100,
        'total_following': 50
    })
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_should_follow(self, login_fn, get_user_info_fn, occurrence_fn):
        self.bot.login()
        username = 'Foo'
        self.assertTrue(self.bot._should_follow(username))
        self.assertTrue(self.bot._should_follow(username, min_followers=50))
        self.assertTrue(self.bot._should_follow(username, max_followers=100))
        self.assertTrue(self.bot._should_follow(
            username, min_followers=50, max_followers=101))
        self.assertFalse(self.bot._should_follow(username, min_followers=150))
        self.assertFalse(self.bot._should_follow(username, max_followers=90))
        self.assertFalse(self.bot._should_follow(
            username, min_followers=50, max_followers=90))
        self.assertFalse(self.bot._should_follow(
            username, ignore_users=(username,)))

    @patch('pyinstamation.bot.InstaBot.probability_of_occurrence', return_value=True)
    def test_should_like(self, occurrence_fn):
        self.bot.likes_given_by_bot = 10
        self.bot.likes_per_day = 100
        self.assertTrue(self.bot._should_like())

        self.bot.likes_given_by_bot = 100
        self.assertFalse(self.bot._should_like())

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.like', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_like(self, login_fn, like_fn):
        self.bot.login()
        self.bot.like('post_link')
        self.assertEqual(self.bot.likes_given_by_bot, 1)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unlike', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_unlike(self, login_fn, unlike_fn):
        self.bot.login()
        self.bot.unlike('post_link')
        self.assertEqual(self.bot.unlikes_given_by_bot, 1)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unlike', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_unlike_multiple_posts(self, login_fn, unlike_fn):
        self.bot.login()
        self.bot.unlike_multiple_posts(['post_1', 'post_2'])
        self.assertEqual(self.bot.unlikes_given_by_bot, 2)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.like', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_like_multiple_posts(self, login_fn, like_fn):
        self.bot.login()
        self.bot.like_multiple_posts(['post_1', 'post_2'])
        self.assertEqual(self.bot.likes_given_by_bot, 2)

    @patch('pyinstamation.bot.InstaBot.probability_of_occurrence', return_value=True)
    def test_should_comment(self, occurrence_fn):
        self.bot.comment_enabled = False
        self.assertFalse(self.bot._should_comment())

        self.bot.comment_enabled = True
        self.bot.comments_per_day = 100
        self.bot.commented_post = 10
        self.assertTrue(self.bot._should_comment())

        self.bot.commented_post = 100
        self.assertFalse(self.bot._should_comment())

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.comment', return_value=True)
    def test_comment(self, comment_fn):
        self.bot.comment('post_link', 'comment')
        self.assertEqual(self.bot.commented_post, 1)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.comment', return_value=True)
    def test_comment_multiple_posts(self, comment_fn):
        posts = [
            {
                'post': 'https://www.instagram.com/p/BXamBMihdBF/',
                'comment': 'very nice'
            },
            {
                'post': 'https://www.instagram.com/p/BXamBMihkdki9/',
                'comment': '#awesome #trip'
            },
            {}

        ]

        self.bot.comment_multiple_posts(posts)
        self.assertEqual(self.bot.commented_post, 2)

    def test_validate_post(self):
        self.assertTrue(self.bot._validate_post('_'))
        post = {
            'caption': '#hola #argentina'
        }
        self.assertFalse(self.bot._validate_post(post, ['hola']))
        self.assertTrue(self.bot._validate_post(post, ['netherlands']))
