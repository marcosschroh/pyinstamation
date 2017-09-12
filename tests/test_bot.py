import random
import unittest
import json
from datetime import datetime
from unittest.mock import patch

from pyinstamation.scrapper.insta_scrapper import InstaScrapper
from pyinstamation import config
from pyinstamation.bot import InstaBot, FollowedUser


POSTS = '[{"dimensions": {"height": 1080, "width": 1080}, "is_video": false, "likes": {"count": 1}, "comments_disabled": false, "code": "BY4PleaDEzx", "owner": {"id": "5604411695"}, "id": "1601098213497785585", "caption": "Gothomefromaweekendawayandfoundthesebabysnakeplantspoppingup.", "thumbnail_resources": [], "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/21577246_2092120784147375_3122997589960556544_n.jpg", "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21577246_2092120784147375_3122997589960556544_n.jpg", "comments": {"count": 0}, "date": 1505085802}, {"dimensions": {"height": 480, "width": 480}, "is_video": false, "likes": {"count": 2}, "comments_disabled": false, "code": "BY4Pd60ja4I", "owner": {"id": "3415217960"}, "id": "1601097694251429384", "caption": "Hopesandaspirationsremainadreamuntilwedosomethingaboutit #contemporaryart#artgallery#wallart", "thumbnail_resources": [], "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/21569163_495461224153455_8943053518743273472_n.jpg", "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/21569163_495461224153455_8943053518743273472_n.jpg", "comments": {"count": 1}, "date": 1505085740}, {"dimensions": {"height": 1080, "width": 1080}, "is_video": false, "likes": {"count": 2}, "comments_disabled": false, "code": "BY4PHmghsHS", "owner": {"id": "1400369852"}, "id": "1601096160612106706", "caption": "#miyazaki#haku#prism#notmyart#moving#apartmentdecor#apartment#art", "thumbnail_resources": [], "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/21576753_1649063248459367_5787605419341905920_n.jpg", "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21576753_1649063248459367_5787605419341905920_n.jpg", "comments": {"count": 0}, "date": 1505085557}, {"dimensions": {"height": 1080, "width": 1080}, "is_video": false, "likes": {"count": 5}, "comments_disabled": false, "code": "BY4O_DDjDtg", "owner": {"id": "3415217960"}, "id": "1601095572789148512", "caption": "Whenweusearttoexpressou #wallart", "thumbnail_resources": [], "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/21576657_1968381606782975_1784797711669657600_n.jpg", "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21576657_1968381606782975_1784797711669657600_n.jpg", "comments": {"count": 0}, "date": 1505085487}, {"dimensions": {"height": 480, "width": 480}, "is_video": false, "likes": {"count": 1}, "comments_disabled": false, "code": "BY4Ne9Wjg0G", "owner": {"id": "5958382806"}, "id": "1601088969595817222", "caption": "Over the weekend Imadeavisionboardandt", "thumbnail_resources": [], "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/21480158_1108015039334954_4616756648227110912_n.jpg", "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/e35/21480158_1108015039334954_4616756648227110912_n.jpg", "comments": {"count": 1}, "date": 1505084700}]'
USERNAME = 'username'
PASSWORD = 'password'


class BotTestCase(unittest.TestCase):

    def setUp(self):
        config.load_config(filepath='test.config.yaml')
        self.scrapper = InstaScrapper(hide_browser=True)
        self.bot = InstaBot(self.scrapper, username=USERNAME, password=PASSWORD)
        self.hashtag = 'apartmentdecor'
        self.hashtag_dict = {
            'hashtag': 'architecture',
            'min_followers': 0,
            'total_to_follow': 20
        }
        self.users_to_unfollow = [
            FollowedUser('juan', None),
            FollowedUser('miguel', None)
        ]
        self.hashtags = [self.hashtag, self.hashtag_dict]

    def test_bot_username_and_password_from_config(self):
        bot = InstaBot(self.scrapper)
        self.assertEqual(bot.username, config.CONFIG.get('username'))
        self.assertEqual(bot.password, config.CONFIG.get('password'))

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_login(self, login_fn):
        self.bot.login()
        self.assertEqual(self.bot.user_login, True)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.logout', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_logout(self, login_fn, logout_fn):
        self.bot.login()
        self.assertTrue(self.bot.logout())

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.logout', return_value=True)
    def test_logout_no_login(self, logout_fn):
        self.assertTrue(self.bot.logout())

    @patch('random.uniform', return_value=0.5)
    def test_probability_of_occurrence(self, uniform_fn):
        self.assertTrue(self.bot.probability_of_occurrence(0.6))
        self.assertFalse(self.bot.probability_of_occurrence(0.4))

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.user_info', return_value={
        'total_followers': 100,
        'total_following': 50
    })
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_my_profile_info(self, login_fn, user_info_fn):
        self.bot.login()
        self.bot.my_profile_info()
        self.assertEqual(self.bot.total_followers, 100)
        self.assertEqual(self.bot.total_following, 50)

    def test_user_info_no_login(self):
        r = self.bot.user_info('no_real_username')
        self.assertEqual(r, {})

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

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.upload_picture', return_value=True)
    def test_picture_step(self, upload_picture_fn):
        self.bot.upload = True
        self.bot.pictures = [
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

        self.bot.picture_step()
        self.assertEqual(self.bot.pictures_uploaded, 2)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unfollow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_unfollow_user(self, login_fn, unfollow_user_fn):
        self.bot.login()

        username = 'Foo'
        self.bot.unfollow(username)
        self.assertTrue(
            len([u for u in self.bot.users_unfollowed_by_bot if u.username == username])
        )

    def test_unfollow_no_login(self):
        username = 'Foo'
        result = self.bot.unfollow(username)
        self.assertFalse(result)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unfollow', return_value=True)
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

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.user_info', return_value={
        'total_followers': 100,
        'total_following': 50
    })
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.follow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_follow_user(self, login_fn, follow_user_fn, user_info_fn):
        self.assertFalse(self.bot.follow(''))
        self.bot.login()

        username = 'Bar'
        self.bot.follow(username)
        self.assertTrue(
            len([u for u in self.bot.users_followed_by_bot if u.username == username])
        )

        self.assertFalse(self.bot.follow(
            username, conditions_checked=False, min_followers=101))

    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.follow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_follow_multiple_users(self, login_fn, follow_user_fn, should_follow_fn):
        self.bot.login()
        self.bot.follow_multiple_users(['user1', 'user2'])
        self.assertEqual(self.bot.total_user_followed_by_bot, 2)

    @patch('pyinstamation.bot.InstaBot.probability_of_occurrence', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.user_info', return_value={
        'total_followers': 100,
        'total_following': 50
    })
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_should_follow(self, login_fn, user_info_fn, occurrence_fn):
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

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_should_follow_not_enabled(self, login_fn):
        self.bot.login()
        self.bot.follow_enable = False
        username = 'Foo'
        self.assertFalse(self.bot._should_follow(username))

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_should_follow_users_followed_more_than_follow_per_day(self, login_fn):
        self.bot.login()
        self.bot.total_user_followed_by_bot = 10
        self.bot.follow_per_day = 5
        username = 'Foo'
        self.assertFalse(self.bot._should_follow(username))

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

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.comment', return_value=True)
    def test_comment_multiple_posts_no_comment(self, comment_fn):
        posts = [
            {
                'post': 'https://www.instagram.com/p/BXamBMihdBF/',
                'comment': ''
            },
            {
                'post': 'https://www.instagram.com/p/BXamBMihkdki9/',
                'comment': '#awesome #trip'
            },
            {}

        ]

        self.bot.comment_multiple_posts(posts)
        self.assertEqual(self.bot.commented_post, 1)

    def test_validate_post(self):
        self.assertTrue(self.bot._validate_post('_'))
        post = {
            'caption': '#hola #argentina'
        }
        self.assertFalse(self.bot._validate_post(post, ['hola']))
        self.assertTrue(self.bot._validate_post(post, ['netherlands']))

    def test_start_browser(self):
        self.bot.start_browser()
        self.assertIsNotNone(self.bot.scrapper.browser)
        self.bot.logout()

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unfollow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    def test_unfollow_users_step(self, login_fn, unfollow_user_fn):
        self.bot.login()
        users = [
            FollowedUser('Hi', '_'),
            FollowedUser('Chiche', '_')
        ]

        self.bot.unfollow_users_step(users_to_unfollow=users)
        unfollow_users = [u.username for u in self.bot.users_unfollowed_by_bot]

        self.assertTrue('Hi' in unfollow_users)
        self.assertTrue('Chiche' in unfollow_users)

    def test_comment_issuer_with_generator(self):
        self.bot.comment_generator = True
        random.seed(123)
        comment = self.bot.comment_issuer()
        self.assertEqual(comment, 'this post blew my mind !')

    def test_comment_issuer_with_custom_comments(self):
        self.bot.comment_generator = False
        self.bot.custom_comments = ['awesome']
        comment = self.bot.comment_issuer()
        self.assertEqual(comment, 'awesome')

    def test_comment_issuer_none(self):
        self.bot.comment_generator = False
        self.bot.custom_comments = []
        comment = self.bot.comment_issuer()
        self.assertIsNone(comment)

    def test_ignore_followed(self):
        self.bot.users_following_to_ignore = [FollowedUser(USERNAME, '_')]
        r = self.bot._ignore_followed(USERNAME)
        self.assertTrue(r)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=[])
    def test_explore_hashtag_no_posts(self,
                                      get_hashtag_page_fn,
                                      get_posts_by_hashtag_fn):
        r = self.bot.explore_hashtag(self.hashtag)
        self.assertIsNone(r)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=False)
    def test_explore_hashtag_post_exahausted(self,
                                             get_hashtag_page_fn,
                                             get_posts_by_hashtag_fn,
                                             wait_fn,
                                             username_in_post_page_fn,
                                             should_like_fn,
                                             should_comment_fn,
                                             should_follow_fn):
        r = self.bot.explore_hashtag(self.hashtag, posts_per_hashtag=2)
        self.assertEqual(r, 2)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=False)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=False)
    def test_explore_hashtag_validate_post_fail(self,
                                                get_hashtag_page_fn,
                                                get_posts_by_hashtag_fn,
                                                wait_fn,
                                                username_in_post_page_fn,
                                                should_like_fn,
                                                should_comment_fn,
                                                should_follow_fn,
                                                validate_post_fn):
        r = self.bot.explore_hashtag(self.hashtag, posts_per_hashtag=2)
        self.assertEqual(r, 0)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=False)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=True)
    @patch('pyinstamation.bot.InstaBot._ignore_followed', return_value=True)
    def test_explore_hashtag_ignore_followed(self,
                                             get_hashtag_page_fn,
                                             get_posts_by_hashtag_fn,
                                             wait_fn,
                                             username_in_post_page_fn,
                                             should_like_fn,
                                             should_comment_fn,
                                             should_follow_fn,
                                             validate_post_fn,
                                             ignore_followed_fn):
        r = self.bot.explore_hashtag(self.hashtag, posts_per_hashtag=2)
        self.assertEqual(r, 0)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.like', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=False)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=True)
    @patch('pyinstamation.bot.InstaBot._ignore_followed', return_value=False)
    def test_explore_hashtag_like(self,
                                  login_fn,
                                  get_hashtag_page_fn,
                                  get_posts_by_hashtag_fn,
                                  wait_fn,
                                  username_in_post_page_fn,
                                  like_fn,
                                  should_like_fn,
                                  should_comment_fn,
                                  should_follow_fn,
                                  validate_post_fn,
                                  ignore_followed_fn):
        self.bot.login()
        r = self.bot.explore_hashtag(self.hashtag)
        self.assertEqual(self.bot.likes_given_by_bot, 5)
        self.assertEqual(r, 5)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.comment', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=False)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=True)
    @patch('pyinstamation.bot.InstaBot._ignore_followed', return_value=False)
    def test_explore_hashtag_comment(self,
                                     login_fn,
                                     get_hashtag_page_fn,
                                     get_posts_by_hashtag_fn,
                                     wait_fn,
                                     username_in_post_page_fn,
                                     comment_fn,
                                     should_like_fn,
                                     should_comment_fn,
                                     should_follow_fn,
                                     validate_post_fn,
                                     ignore_followed_fn):
        self.bot.comment_generator = True
        self.bot.login()
        r = self.bot.explore_hashtag(self.hashtag)
        self.assertEqual(self.bot.commented_post, 5)
        self.assertEqual(r, 5)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.follow', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=True)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=True)
    @patch('pyinstamation.bot.InstaBot._ignore_followed', return_value=False)
    def test_explore_hashtag_follow(self,
                                    login_fn,
                                    get_hashtag_page_fn,
                                    get_posts_by_hashtag_fn,
                                    wait_fn,
                                    username_in_post_page_fn,
                                    follow_fn,
                                    should_like_fn,
                                    should_comment_fn,
                                    should_follow_fn,
                                    validate_post_fn,
                                    ignore_followed_fn):
        self.bot.login()
        r = self.bot.explore_hashtag(self.hashtag, total_to_follow=5)
        self.assertEqual(self.bot.total_user_followed_by_bot, 5)
        self.assertEqual(r, 5)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.follow', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=True)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=True)
    @patch('pyinstamation.bot.InstaBot._ignore_followed', return_value=False)
    def test_explore_hashtag_follow_limited(self,
                                            login_fn,
                                            get_hashtag_page_fn,
                                            get_posts_by_hashtag_fn,
                                            wait_fn,
                                            username_in_post_page_fn,
                                            follow_fn,
                                            should_like_fn,
                                            should_comment_fn,
                                            should_follow_fn,
                                            validate_post_fn,
                                            ignore_followed_fn):
        self.bot.login()
        r = self.bot.explore_hashtag(self.hashtag, total_to_follow=2)
        self.assertEqual(self.bot.total_user_followed_by_bot, 2)
        self.assertEqual(r, 2)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.like', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=False)
    def test_explore_hashtag(self, like_fn, login_fn,
                             get_hashtag_page_fn,
                             get_posts_by_hashtag_fn,
                             wait_fn,
                             username_in_post_page_fn,
                             validate_post_fn,
                             should_like_fn, should_comment_fn,
                             should_follow_fn):
        r = self.bot.explore_hashtag(self.hashtag)
        self.assertEqual(r, 5)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.like', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.bot.InstaBot._validate_post', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_like', return_value=True)
    @patch('pyinstamation.bot.InstaBot._should_comment', return_value=False)
    @patch('pyinstamation.bot.InstaBot._should_follow', return_value=False)
    def test_explore_hashtags(self, login_fn, like_fn,
                              get_hashtag_page_fn,
                              get_posts_by_hashtag_fn,
                              wait_fn,
                              username_in_post_page_fn,
                              validate_post_fn,
                              should_like_fn, should_comment_fn,
                              should_follow_fn):
        self.bot.search_tags = self.hashtags
        r = self.bot.explore_hashtags()
        self.assertEqual(r, 4)

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.login', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.like', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.comment', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.follow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.unfollow', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.upload_picture', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=json.loads(POSTS))
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.wait', return_value=None)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.username_in_post_page', return_value=USERNAME)
    @patch('pyinstamation.bot.InstaBot.probability_of_occurrence', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.user_info', return_value={
        'total_followers': 100,
        'total_following': 50
    })
    def test_run(self, login_fn, like_fn, comment_fn, follow_fn, unfollow_fn,
                 upload_picture_fn,
                 get_hashtag_page_fn,
                 get_posts_by_hashtag_fn,
                 wait_fn,
                 username_in_post_page_fn,
                 probability_of_occurrence_fn,
                 user_info_fn):
        self.bot.comment_generator = True
        self.bot.search_tags = self.hashtags
        self.bot.run(users_to_unfollow=self.users_to_unfollow,
                     users_following=[FollowedUser('miguelito', None)])

        self.assertEqual(self.bot.commented_post, 4)
        self.assertEqual(self.bot.total_user_followed_by_bot, 3)
        self.assertEqual(self.bot.likes_given_by_bot, 4)
        self.assertEqual(len(self.bot.users_unfollowed_by_bot), 2)
        self.assertEqual(len(self.bot.users_followed_by_bot), 3)
