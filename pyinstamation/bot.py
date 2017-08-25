import os
import sys
import yaml
import logging
from datetime import datetime
from collections import namedtuple

from pyinstamation.config import CONFIG
from pyinstamation.scrapper import InstaScrapper, instagram_const


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_TEST_PATH = os.path.join(BASE_DIR, 'scrapper', 'chiche.jpg')
FollowedUser = namedtuple('FollowedUser', ['username', 'follow_date'])
logger = logging.getLogger(__name__)


def parse_tags(tags):
    """From a given string remove hashtags and spaces.
    :rtype list:
    """
    if tags is None:
        return []
    return tags.replace('#', '').replace(' ', '').split(',')


class InstaBot:

    def __init__(self, username=None, password=None, is_new=True, users_to_unfollow=None,
                 min_followers_for_a_new_follow=100):
        if username is None:
            username = CONFIG.get('username', None)
        if password is None:
            password = CONFIG.get('password', None)
        if users_to_unfollow is None:
            users_to_unfollow = []

        assert username is not None, 'A username must be provided'
        assert password is not None, 'A password must be provided'

        # Configure bot and set default values
        self.username = username
        self.password = password
        self.is_new = is_new
        self.users_to_unfollow = users_to_unfollow

        _posts = CONFIG.get('posts', {})
        self.likes_per_day = _posts.get('likes_per_day', 0)
        self.comment_enabled = _posts.get('comment', False)
        self.search_tags = parse_tags(_posts.get('search_tags', []))
        self.custom_comments = _posts.get('custom_comments', [])
        self.comment_generator = _posts.get('comment_generator', False)
        self.ignore_tags = parse_tags(_posts.get('ignore_tags', None))
        self.total_to_follow_per_hashtag = _posts.get('total_to_follow_per_hashtag')
        self.posts_per_hashtag = _posts.get('posts_per_hashtag', 2)

        _followers = CONFIG.get('followers', {})
        self.ignore_users = _followers.get('ignore_users', [])
        self.follow_enable = _followers.get('follow_enable', False)
        self.min_followers = _followers.get('min_followers', 0)
        self.max_followers = _followers.get('max_followers', 0)
        self.follow_per_day = _followers.get('follow_per_day', 10)
        self.ignore_friends = _followers.get('ignore_friends', True)
        
        _pictures_config = CONFIG.get('pics', {})
        self.upload = _pictures_config.get('upload', False)
        self.pictures = _pictures_config.get('files', [])
        self.pictures_uploaded = 0

        # End configuration

        # Bot internal states
        self._user_login = False

        # Bot statistics
        self.commented_post = 0
        self.total_followers = 0
        self.total_following = 0
        self.likes_given_by_bot = 0
        self.min_followers_for_a_new_follow = min_followers_for_a_new_follow
        self.users_followed_by_bot = []
        self.users_unfollowed_by_bot = []
        self.total_user_followed_by_bot = 0

        self.scrapper = InstaScrapper()
        self._configure_log()
        self._reach_website()

    def _reach_website(self):
        self.scrapper.reach_website()

    def _configure_log(self):
        logger.info('Hiiiii bot....')

    def login(self):
        if self.scrapper.login(self.username, self.password):
            self._user_login = True

    def logout(self):
        if self.user_login:
            self.scrapper._get_my_profile_page()
            self.scrapper.logout()
        else:
            logger.info('login first alsjeblieft')

    def _get_my_profile_page(self):
        self.scrapper.get_my_profile_page(self.username)

    @property
    def user_login(self):
        return self._user_login

    def upload_picture(self, image_path, comment=None):
        self.scrapper.upload_picture(image_path, comment)

    def upload_multiple_pictures(self, pictures_list):
        """
        @pictures_list: list of dictionaries, where each dictionary
        represent an image to upload.

        [
            {
                'file': 'path to file',
                'comment': '#nice',
            },
            {
                'hashtag': 'path to another file'
            }

            ...
        ]
        """
        for picture in pictures_list:
            pic = picture.get('path')
            print(pic)
            comment = picture.get('comment', None)
            self.upload_picture(pic, comment)
            self.pictures_uploaded += 1

    def follow_user(self, username, conditions_checked=True, min_followers=None, max_followers=None):
        if self.user_login:

            if not conditions_checked:
                if not self._check_follow_conditions(username, min_followers=min_followers, max_followers=max_followers):
                    return False

            if self.scrapper.follow_user(username):
                self.users_followed_by_bot.append(
                    FollowedUser(
                        username=username,
                        follow_date= datetime.utcnow()
                    )
                )
                self.total_following += 1
                self.total_user_followed_by_bot += 1
                return True

        return False

    def follow_multiple_users(self, username_list, min_followers=None, max_followers=None):
        for username in username_list:
            self.follow_user(
                username,
                conditions_checked=False,
                min_followers=min_followers,
                max_followers=max_followers
            )

    def unfollow_user(self, username):
        if self._user_login:
            if self.scrapper.unfollow_user(username):
                self.users_unfollowed_by_bot.append(
                    FollowedUser(
                        username=username,
                        follow_date= datetime.utcnow()
                    )
                )
                self.total_following -= 1

    def unfollow_multiple_users(self, username_list):
        for username in username_list:
            self.unfollow_user(username)

    def get_user_info(self, username):
        if self._user_login:
            return self.scrapper.get_user_info(username)

    def _check_follow_conditions(self, username, min_followers=None, max_followers=None, ignore_users=None):
        if min_followers or max_followers:
            user_info = self.get_user_info(username)
            user_followers = user_info.get('total_followers', 0)

            if not max_followers:
                max_followers = instagram_const.TOTAL_MAX_FOLLOWERS

            if not (min_followers <= user_followers <= max_followers):
                return False

            if ignore_users and username in ignore_users:
                return False

        return True

    def get_my_profile_info(self):
        if self._user_login:
            my_profile = self.get_user_info(self.username)
            self.total_followers = my_profile.get('total_followers')
            self.total_following = my_profile.get('total_following')

    def follow_users_by_hashtag(self, hashtag, min_followers=None, total_to_follow=1, ignore_users=None, posts_per_hashtag=None):
        self.scrapper.get_hashtag_page(hashtag)
        posts = self.scrapper.get_posts_by_hashtag(hashtag)

        if not posts:
            logger.info('No posts were found for HASHTAG {0}'.format(hashtag))
            return

        users_followed_by_hashtag = 0
        for i, post in enumerate(posts, 1):
            # if there is a posts there is a code....
            post_code = post.get('code')
            post_url = self.scrapper.generate_post_link_by_code(post_code)
            
            self.scrapper.wait(sleep_time=3)
            username = self.scrapper.get_username_in_post_page(post_url)

            if self.likes_given_by_bot < self.likes_per_day:
                self.like_post(post_url)

            if self.comment_enabled:
                # think aboit the comment generator and comment per post...
                # self.commented_post(post_url)
                pass

            if self.follow_enable and self.total_user_followed_by_bot < self.follow_per_day \
                    and users_followed_by_hashtag < total_to_follow:

                if self._check_follow_conditions(username, min_followers=min_followers, ignore_users=ignore_users):
                    if self.follow_user(username):
                        users_followed_by_hashtag += 1

            if posts_per_hashtag and posts_per_hashtag <= i:
                break

    def follow_users_by_multiple_hashtags(self, hashtags, min_followers=None, total_to_follow=1, ignore_users=None, posts_per_hashtag=None):
        """
        @hashtags: list of dictionaries where every dict
        contains:
            @hashtag: str that represent the hashtag
            @total_to_follow: int that represent total of user to follow
            @min_followers: only follow the user if has at least
            min_followers

        Important: Do not include # in every hashtag

        E.g.

        List of dictionaries:
        [
            {
                'hashtag': 'haarlem',
                'min_followers': 20,
                'total_to_follow': 10
            },
            {
                'hashtag': 'python',
                'min_followers': 20,
                'total_to_follow': '15'
            },
            {
                'hashtag': 'flask',
                'min_followers': 60,
                'total_to_follow': 1
            }

            ...
        ]

        If you do not provide a min_followers or total_to_follow
        per each dict it will try to use the min_followers and
        total_to_follow parameters.
        """

        for hashtag_data in hashtags:
            hashtag = hashtag_data
            if type(hashtag_data) is dict:
                hashtag = hashtag_data.get('hashtag')
                min_followers = hashtag_data.get('min_followers', min_followers)
                total_to_follow = hashtag_data.get('total_to_follow', total_to_follow)
    
            self.follow_users_by_hashtag(
                hashtag, 
                min_followers=min_followers,
                total_to_follow=total_to_follow,
                ignore_users=ignore_users,
                posts_per_hashtag=posts_per_hashtag
            )

    def like_post(self, post_link):
        if self._user_login:
            if self.scrapper.like_post(post_link):
                self.likes_given_by_bot += 1

    def unlike_post(self, post_link):
        if self._user_login:
            if self.scrapper.unlike_post(post_link):
                self.likes_given_by_bot -= 1

    def like_multiple_posts(self, post_link_list):
        for post in post_link_list:
            self.like_post(post)

    def unlike_multiple_posts(self, post_link_list):
        for post in post_link_list:
            self.unlike_post(post)

    def comment_post(self, post_link, comment):
        if self.scrapper.comment_post(post_link, comment):
            self.commented_post += 1

    def comment_multiple_posts(self, posts_list, default_comment=None):
        """
        Expect a list of dictionaries where every dict
        has the post link and the comment.

        E.g.

        [
            {
                'post': 'https://www.instagram.com/p/BXamBMihdBF/'
                'comment': 'very nice'
            },
            {
                'post': 'https://www.instagram.com/p/BXamBMihkdki9/'
                'comment': '#awesome #trip'
            },

            ...

        ]

        If a dict has not the attribute comment it tries to use the
        default_comment key. If the default_comment is not present,
        just skip.
        """

        current_commented_posts = self.commented_post

        for post_object in posts_list:
            post = post_object.get('post')
            comment = post_object.get('post', default_comment)

            if not post or not comment:
                continue

            self.comment_post(post, comment)

        total_comments_made = self.commented_post - current_commented_posts
        logger.info('Commented {0} of {1}'.format(total_comments_made, len(posts_list)))

    def find_by_hashtag(self, hashtag):
        if self._user_login:
            self.scrapper.find_by_hashtag(hashtag)

    def picture_step(self):
        if self.upload:
            self.upload_multiple_pictures(self.pictures)

    def unfollow_users_step(self):
        self.unfollow_multiple_users(self.users_to_unfollow)

    def follow_users_step(self):
        """
        Start the real step.

        1. Search by hashtags

        """
        self.follow_users_by_multiple_hashtags(
            self.search_tags,
            min_followers=self.min_followers_for_a_new_follow,
            total_to_follow=self.total_to_follow_per_hashtag,
            ignore_users=self.ignore_users,
            posts_per_hashtag=self.posts_per_hashtag
        )

    def run(self):
        """
        1. login
        2. pics
        3. unfollow users
        4. follow process
            per post
            me gusta
            comment probability
            follow probability
        """
        self.login()
        self.picture_step()
        self.unfollow_users_step()
        self.follow_users_step()

        
