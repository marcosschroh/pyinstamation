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

    def __init__(self, username=None, password=None, is_new=True, unfollow_users=None,
                 min_followers_for_a_new_follow=100):
        if username is None:
            username = CONFIG.get('username', None)
        if password is None:
            password = CONFIG.get('password', None)
        if unfollow_users is None:
            unfollow_users = []

        assert username is not None, 'A username must be provided'
        assert password is not None, 'A password must be provided'

        # Configure bot and set default values
        self.username = username
        self.password = password
        self.is_new = is_new
        self.unfollow_users = unfollow_users

        _posts = CONFIG.get('posts', {})
        self.likes = _posts.get('likes', 0)
        self.comment = _posts.get('comment', False)
        self.search_tags = parse_tags(_posts.get('search_tags', None))
        self.custom_comments = _posts.get('custom_comments', [])
        self.comment_generator = _posts.get('comment_generator', False)
        self.ignore_pics_with_tags = parse_tags(_posts.get('ignore_pics_with_tags', None))

        _followers = CONFIG.get('followers', {})
        self.ignore_users = _followers.get('ignore_users', [])
        self.follow_enable = _followers.get('follow_enable', False)
        self.min_followers = _followers.get('min_followers', 0)
        self.max_followers = _followers.get('max_followers', 0)
        self.follow_per_day = _followers.get('follow_per_day', 10)
        self.ignore_friends = _followers.get('ignore_friends', True)
        # End configuration

        # Bot internal states
        self._user_login = False

        # Bot statistics
        self.commented_post = 0
        self.total_followers = 0
        self.total_following = 0
        self.likes_given_with_bot = 0
        self.min_followers_for_a_new_follow = min_followers_for_a_new_follow
        self.users_followed_by_bot = []
        self.users_unfollowed_by_bot = []

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

    def upload_picture(self, image_path, comment):
        self.scrapper.upload_picture(image_path, comment)

    def start(self):
        pass

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

    def _check_follow_conditions(self, username, min_followers=None, max_followers=None):
        if min_followers or max_followers:
            user_info = self.get_user_info(username)
            user_followers = user_info.get('total_followers', 0)

            if not max_followers:
                max_followers = instagram_const.TOTAL_MAX_FOLLOWERS

            if not (min_followers <= user_followers <= max_followers):
                return False

        return True

    def get_my_profile_info(self):
        if self._user_login:
            my_profile = self.get_user_info(self.username)
            self.total_followers = my_profile.get('total_followers')
            self.total_following = my_profile.get('total_following')

    def follow_users_by_hashtag(self, hashtag, min_followers=None, total_to_follow=1):
        self.scrapper.get_hashtag_page(hashtag)
        posts = self.scrapper.get_posts_by_hashtag(hashtag)

        if not posts:
            logger.info('No posts were found for HASHTAG {0}'.format(hashtag))
            return

        for i, post in enumerate(posts, 1):
            # if there is a posts there is a code....
            post_code = post.get('code')
            post_url = self.scrapper.generate_post_link_by_code(post_code)
            username = self.scrapper.get_username_in_post_page(post_url)

            if self._check_follow_conditions(username, min_followers=min_followers):
                self.like_post(post_url)
                self.follow_user(username)

            if i == total_to_follow:
                break

    def like_post(self, post_link):
        if self._user_login:
            if self.scrapper.like_post(post_link):
                self.likes_given_with_bot += 1

    def unlike_post(self, post_link):
        if self._user_login:
            if self.scrapper.unlike_post(post_link):
                self.likes_given_with_bot -= 1

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

    def run(self):
        pass


if __name__ == '__main__':
    with open("config.yaml", 'r') as stream:
        try:
            CONFIG = yaml.load(stream)
        except yaml.YAMLError as exc:
            sys.exit(exc)

    bot = InstaBot(CONFIG.get('username'), CONFIG.get('password'))

    # actions
    bot.login()
    # bot.get_user_info('woile')
    # bot.get_my_profile_info()
    # bot.follow_user('woile', min_followers=0, max_followers=0)
    # bot.follow_multiple_users(['woile', 'marcosschroh'])
    # bot.unfollow_user('woile')
    # bot.unfollow_muliple_users(['woile', 'marcosschroh'])
    # bot.like_post('https://www.instagram.com/p/BXamBMihdBF/')
    # bot.like_multiple_posts(['https://www.instagram.com/p/BXamBMihdBF/'])
    # bot.unlike_post('https://www.instagram.com/p/BXamBMihdBF/')
    # bot.unlike_multiple_posts(['https://www.instagram.com/p/BXamBMihdBF/'])
    # bot.upload_picture(IMAGE_TEST_PATH, '#chiche #bombom #pp')
    # bot.follow_users_by_hashtag('haarlem', min_followers=None, total_to_follow=1)
