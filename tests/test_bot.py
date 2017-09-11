import unittest
import json
from datetime import datetime
from unittest.mock import patch

from pyinstamation.scrapper.insta_scrapper import InstaScrapper
from pyinstamation import config
from pyinstamation.bot import InstaBot, FollowedUser


POSTS = '{"user": {"username": "discovrar", "saved_media": {"page_info": {"has_next_page": false, "end_cursor": null}, "count": 0, "nodes": []}, "follows": {"count": 74}, "follows_viewer": false, "blocked_by_viewer": false, "external_url": null, "profile_pic_url_hd": "https://scontent-ams3-1.cdninstagram.com/t51.2885-19/s320x320/20759907_669008043293056_6297997226601873408_a.jpg", "id": "5845752529", "media": {"page_info": {"has_next_page": false, "end_cursor": "AQDotpGXCTDnDTX9Z4COD2hGwraavaEg5xI5Dje8KEMsePlmrl3E8T7kN2Fc6ktSGOs"}, "count": 5, "nodes": [{"date": 1504907908, "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21435528_496506830727569_1888902354510544896_n.jpg", "comments": {"count": 0}, "__typename": "GraphImage", "caption": "#go #motivation", "comments_disabled": false, "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s1080x1080/e15/fr/21435528_496506830727569_1888902354510544896_n.jpg", "id": "1599605936640756021", "media_preview": "ACoq6Giiq32ggkFGIB7f1zjr1GCeDQBZoqsbnAU7G+bJPHI6/wCfoc0v2kYztbggEY5zjP8ALH4nHrQBYopFOQD0z29KWgAqKV5FxsXd68/561LVYicE4KsO2eDjt07+9ACiWQg/JyMcZ9Rk/lwPr9KckkhbDJtGOoOefT/6/rTWE+7K7NvHXP4/r+lMIuOxT8fp/jzx+NAFuikGcc9e9LQAUUUUAFFFFADWbFOoooA//9k=", "code": "BYy8R_SFAk1", "dimensions": {"width": 1080, "height": 1080}, "is_video": false, "gating_info": null, "likes": {"count": 1}, "thumbnail_resources": [], "owner": {"id": "5845752529"}}, {"date": 1504178194, "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21149364_1530343790365779_4203733536273858560_n.jpg", "comments": {"count": 0}, "__typename": "GraphImage", "caption": "#motivation #getmotivated #phraseoftheday", "comments_disabled": false, "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s1080x1080/e15/fr/21149364_1530343790365779_4203733536273858560_n.jpg", "id": "1593484647018213683", "media_preview": "ACoq6Giiq3nkEgoxAPb8eucdeowTwaALNFVjc4CnY3zZJ45HX/P0OaX7SMZ2twQCMc5xn+WPxOPWgCxRSKcgHpnt6UtABUUryLjYu715/wA9alqsROCcFWHbPBx2HHf3oAUSyEH5ORjjPqMn8uB9fpTkkkLYZNox1Bzz6f4n1prCfdldm3jrn8f1/SmkXHYp+P0/x54/GgC1RSDOOeveloAKKKKACiiigBrHFOoooA//2Q==", "code": "BYdMdgEjzEz", "dimensions": {"width": 1080, "height": 1080}, "is_video": false, "gating_info": null, "likes": {"count": 4}, "thumbnail_resources": [], "owner": {"id": "5845752529"}}, {"date": 1503691720, "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/e15/c0.0.1079.1079/21041245_138874340051868_4493522014891409408_n.jpg", "comments": {"count": 0}, "__typename": "GraphImage", "caption": "#chichelogo #bombom", "comments_disabled": false, "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s1080x1080/e15/fr/21041245_138874340051868_4493522014891409408_n.jpg", "id": "1589403804570509344", "media_preview": "ACop5mlpKKAFooxSYoAKKKKAClpKKAFopKKAClpKWgBKWkooAWiig0AJRRRQB//Z", "code": "BYOslbYFGAg", "dimensions": {"width": 1080, "height": 1079}, "is_video": false, "gating_info": null, "likes": {"count": 3}, "thumbnail_resources": [], "owner": {"id": "5845752529"}}, {"date": 1503690754, "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21107946_987697158036559_3672536087093313536_n.jpg", "comments": {"count": 0}, "__typename": "GraphImage", "caption": "#chicheisback #bombom", "comments_disabled": false, "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s1080x1080/e15/fr/21107946_987697158036559_3672536087093313536_n.jpg", "id": "1589395700613322217", "media_preview": "ACoqxM1vJFtjT/dH6/8A66yTdswxtT/vhf8ACtqSUKRGQVxjnsMd89O1aSdlqKKu9CRrUBc96qDkZq1McDBduo9MdOnrjpVLeBlRnIBOe3r1rKEtbNmk46XSMSc5c/57VcW1hIBMoBI9RVZ5TvOAOvoKd9ob0X/vkf4V0NN7O33GV7dB7w+WAdyNz0Ukn69BUUkryn52LfUk0mw4yBmos5GazbGdBFMJI48njo5xkgjjg9sjnnp+IFYPmMCSpIBJ6Gp45CEYAZ7g+meDx3z09qrMMAH1H9ai1tim29yRY9/JYDPrn/Cpfs4/vr+v+FVaXca6IvT/AIBmzRXanHUIM9M9ffHr1z0pNPsReOV3bQoznGe+MVptIxyCSR9TTrThjj0rlcrPlt8zVK6uV5tMSCPKhpm+u3j2ABzj05rImtyFEiZMbjIPcY6g/Q9+45robonyW9hkexB4/LtVOMknk55/n1oTKaMeOQJnIDfX/wDUam+1j/nmn5D/AAqmOlFboyP/2Q==", "code": "BYOqvf-lxXp", "dimensions": {"width": 1080, "height": 1080}, "is_video": false, "gating_info": null, "likes": {"count": 2}, "thumbnail_resources": [], "owner": {"id": "5845752529"}}, {"date": 1502225019, "thumbnail_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/20635180_1345692435548582_4416221017404342272_n.jpg", "comments": {"count": 1}, "__typename": "GraphImage", "caption": "#chiche #bombom #pp", "comments_disabled": false, "display_src": "https://scontent-ams3-1.cdninstagram.com/t51.2885-15/s1080x1080/e15/fr/20635180_1345692435548582_4416221017404342272_n.jpg", "id": "1577100224870245023", "media_preview": "ACoq5/yG9vzpVt2Y4GM1okyY6H8v/rUlqu+TBHY9qtoVyn9ik9vzqB4ijbTjIrpPL9qjjto2dmkxx0GBnoOc9TUbblb7GB5LYzxxUeK05Znjc7B+O3tVDP8Asj9f8aqxJ0kc5giiVFRy4Ykn2Y96khuRM7JIiIQp+ZeD09fyp8MatGEJQbRgZBzjr6+vepHgUggMqhuGwuc/iSef5VnfUq2hl3U6j5ISWduOCSBn09T6enWq1ndeWjByTgEr7k8YPtnr37VtR28MIwnUjBbqf8/TH0rHms0A/dZHPJJJ4+mKLoNSgNzZyxHfv/So/wDgX861o9OI53rgj0b9eKjOnH+9H/49VXQrMaNSUdVPr1x7+h4qf+2h/c/8e/8ArVhUVPKh3Zvf20P7h/76/wDrUDWx/cP/AH1/9asGijlQ7s6D+2k7ofzH+FH9sx/3G/MVz9FLlQXZ/9k=", "code": "BXi_Ex2lGKf", "dimensions": {"width": 1080, "height": 1080}, "is_video": false, "gating_info": null, "likes": {"count": 3}, "thumbnail_resources": [], "owner": {"id": "5845752529"}}]}, "biography": null, "country_block": false, "is_verified": false, "has_requested_viewer": false, "profile_pic_url": "https://scontent-ams3-1.cdninstagram.com/t51.2885-19/s150x150/20759907_669008043293056_6297997226601873408_a.jpg", "followed_by_viewer": false, "full_name": "Discovr", "requested_by_viewer": false, "followed_by": {"count": 16}, "external_url_linkshimmed": null, "is_private": false, "connected_fb_page": null, "has_blocked_viewer": false}, "logging_page_id": "profilePage_5845752529"}'


class BotTestCase(unittest.TestCase):

    def setUp(self):
        config.load_config(filepath='test.config.yaml')
        username = 'username'
        password = 'password'
        self.scrapper = InstaScrapper(hide_browser=True)
        self.bot = InstaBot(self.scrapper, username=username, password=password)
        self.hashtag = 'apartmentdecor'

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

    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_hashtag_page', return_value=True)
    @patch('pyinstamation.scrapper.insta_scrapper.InstaScrapper.get_posts_by_hashtag', return_value=[])
    def test_explore_hashtag_no_posts(self,
                                     get_hashtag_page_fn,
                                     get_posts_by_hashtag_fn):
        r = self.bot.explore_hashtag(self.hashtag)
        self.assertIsNone(r)
