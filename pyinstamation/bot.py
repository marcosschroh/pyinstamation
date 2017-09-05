import os
import logging
import random
from datetime import datetime
from collections import namedtuple

from pyinstamation.config import CONFIG
from pyinstamation.scrapper import instagram_const
from pyinstamation import comments

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_TEST_PATH = os.path.join(BASE_DIR, 'scrapper', 'chiche.jpg')
FollowedUser = namedtuple('FollowedUser', ['username', 'follow_date'])
logger = logging.getLogger(__name__)


def remove_hashtags(tags):
    return map(lambda x: x.replace('#', ''), tags)


class InstaBot:

    def __init__(self, scrapper, username=None, password=None, is_new=True,
                 min_followers_for_a_new_follow=100):
        if username is None:
            username = CONFIG.get('username', None)
        if password is None:
            password = CONFIG.get('password', None)

        assert username is not None, 'A username must be provided'
        assert password is not None, 'A password must be provided'

        # Configure bot and set default values
        self.username = username
        self.password = password
        self.is_new = is_new

        _posts = CONFIG.get('posts', {})
        self.likes_per_day = _posts.get('likes_per_day', 0)
        self.like_probability = _posts.get('like_probability', 0.5)
        self.comments_per_day = _posts.get('comments_per_day', 0)
        self.comment_enabled = _posts.get('comment_enabled', False)
        self.comment_generator = _posts.get('comment_generator', False)
        self.comment_probability = _posts.get('comment_probability', 0.5)
        self.search_tags = remove_hashtags(_posts.get('search_tags', []))
        self.custom_comments = _posts.get('custom_comments', [])
        self.ignore_tags = remove_hashtags(_posts.get('ignore_tags', []))
        self.total_to_follow_per_hashtag = _posts.get('total_to_follow_per_hashtag', 10)
        self.posts_per_hashtag = _posts.get('posts_per_hashtag', )

        _followers = CONFIG.get('followers', {})
        self.ignore_users = _followers.get('ignore_users', [])
        self.follow_enable = _followers.get('follow_enable', False)
        self.min_followers = _followers.get('min_followers', 0)
        self.max_followers = _followers.get('max_followers', 0)
        self.follow_per_day = _followers.get('follow_per_day', 50)
        self.ignore_friends = _followers.get('ignore_friends', True)
        self.follow_probability = _followers.get('follow_probability', 0.5)

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
        self.unlikes_given_by_bot = 0
        self.min_followers_for_a_new_follow = min_followers_for_a_new_follow
        self.users_followed_by_bot = []
        self.users_unfollowed_by_bot = []
        self.total_user_followed_by_bot = 0

        # represent the users that you are already following
        # this result comes from the Controller
        self.users_following_to_ignore = []

        self.scrapper = scrapper

    @staticmethod
    def parse_caption(caption):
        return map(
            lambda x: x.replace('#', ''),
            (filter(lambda h: h.startswith("#"), caption.split(' ')))
        )

    @staticmethod
    def probability_of_occurrence(probability):
        """
        :type threshold: float
        """
        r = random.uniform(0, 1)
        msg = 'Random {0} should be lower than probability {1}'
        logger.info(msg.format(r, probability))
        return r <= probability

    def login(self):
        if self.scrapper.login(self.username, self.password):
            self._user_login = True

    def logout(self):
        if self.user_login:
            self.scrapper.logout()
            self._user_login = False
            return True

        logger.info('login first alsjeblieft')
        return False

    @property
    def user_login(self):
        return self._user_login

    def upload_picture(self, image_path, comment=None):
        self.scrapper.upload_picture(image_path, comment)
        self.pictures_uploaded += 1

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
            date_time_str = picture.get('datetime')

            if date_time_str:
                date_time = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")
                if datetime.utcnow().date() != date_time.date():
                    continue

            pic = picture.get('path')
            comment = picture.get('comment', None)
            self.upload_picture(pic, comment)

    def follow_user(self, username, conditions_checked=True, min_followers=None,
                    max_followers=None):
        if self.user_login:

            if not conditions_checked:
                if not self._should_follow(username, min_followers=min_followers,
                                           max_followers=max_followers):
                    return False

            if self.scrapper.follow_user(username):
                self.users_followed_by_bot.append(
                    FollowedUser(
                        username=username,
                        follow_date=datetime.utcnow()
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
                    FollowedUser(username=username, follow_date=datetime.utcnow())
                )
                self.total_following -= 1

    def unfollow_multiple_users(self, users_list):
        """
        :type user_list: iter(Followers)
        """
        for user in users_list:
            self.unfollow_user(user.username)

    def get_user_info(self, username):
        if self._user_login:
            return self.scrapper.get_user_info(username)

    def _validate_post(self, post, ignore_tags=None):
        if not ignore_tags:
            return True

        caption = post.get('caption')
        if caption:
            tags_in_post = self.parse_caption(caption)

            for t in ignore_tags:
                if t in tags_in_post:
                    return False
        return True

    def _should_follow(self, username, min_followers=0, max_followers=None, ignore_users=None):

        if min_followers or max_followers:
            user_info = self.get_user_info(username)
            user_followers = user_info.get('total_followers', 0)

            if not max_followers:
                max_followers = instagram_const.TOTAL_MAX_FOLLOWERS

            if not (min_followers <= user_followers <= max_followers):
                return False

        if ignore_users and username in ignore_users:
            return False

        return self.probability_of_occurrence(self.follow_probability)

    def _should_like(self):
        if not self.likes_given_by_bot < self.likes_per_day:
            logger.info('Likes per day exceeded.')
            return False

        return self.probability_of_occurrence(self.like_probability)

    def _should_comment(self):
        if not self.comment_enabled:
            return False

        if self.comments_per_day <= self.commented_post:
            logger.info('Comments per day exceeded.')
            return False

        return self.probability_of_occurrence(self.comment_probability)

    def get_my_profile_info(self):
        if self._user_login:
            my_profile = self.get_user_info(self.username)
            self.total_followers = my_profile.get('total_followers')
            self.total_following = my_profile.get('total_following')

    def follow_users_by_hashtag(self, hashtag, min_followers=None, total_to_follow=1,
                                ignore_users=None, posts_per_hashtag=None, ignore_tags=None):

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
            if not self._validate_post(post, ignore_tags=ignore_tags):
                msg = 'Ignoring the post {0}. Has at least one hashtag of {1}'
                logger.info(msg.format(post_url, ignore_tags))

            self.scrapper.wait(sleep_time=3)
            username = self.scrapper.get_username_in_post_page(post_url)

            if any(user.username == username for user in self.users_following_to_ignore):
                msg = 'Skip because already following the user {0}'.format(username)
                logger.info(msg)
                continue

            if self._should_like():
                self.like(post_url)

            if self._should_comment():
                if self.comment_generator:
                    comment = comments.generate_comment()
                elif self.custom_comments:
                    comment = random.choice(self.custom_comments)

                if comment:
                    self.comment(post_url, comment)
                    logger.info('Comment to post: {0}'.format(comment))

            if self.follow_enable and self.total_user_followed_by_bot < self.follow_per_day \
                    and users_followed_by_hashtag < total_to_follow:

                if self._should_follow(username, min_followers=min_followers,
                                       ignore_users=ignore_users):
                    if self.follow_user(username):
                        users_followed_by_hashtag += 1

            if posts_per_hashtag and posts_per_hashtag <= i:
                break

    def explore_tags_by_multiple_hashtags(self, hashtags,
                                          min_followers=None,
                                          total_to_follow=1,
                                          ignore_users=None,
                                          posts_per_hashtag=None,
                                          ignore_tags=None):
        """
        :hashtags: collection with the following info:
            :hashtag: str that represent the hashtag
            :total_to_follow: int that represent total of user to follow
            :min_followers: only follow the user if has at least min_followers
        :type hashtags: list
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

            logger.info('Processing hashtag {0}'.format(hashtag))

            self.follow_users_by_hashtag(
                hashtag,
                min_followers=min_followers,
                total_to_follow=total_to_follow,
                ignore_users=ignore_users,
                posts_per_hashtag=posts_per_hashtag,
                ignore_tags=ignore_tags
            )

    def like(self, post_link):
        if self._user_login:
            if self.scrapper.like(post_link):
                self.likes_given_by_bot += 1

    def unlike(self, post_link):
        if self._user_login:
            if self.scrapper.unlike(post_link):
                self.unlikes_given_by_bot += 1

    def like_multiple_posts(self, post_link_list):
        for post in post_link_list:
            self.like(post)

    def unlike_multiple_posts(self, post_link_list):
        for post in post_link_list:
            self.unlike(post)

    def comment(self, post_link, comment):
        if self.scrapper.comment(post_link, comment):
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

            self.comment(post, comment)

        total_comments_made = self.commented_post - current_commented_posts
        logger.info('Commented {0} of {1}'.format(total_comments_made, len(posts_list)))

    def find_by_hashtag(self, hashtag):
        if self._user_login:
            self.scrapper.find_by_hashtag(hashtag)

    def start_browser(self):
        self.scrapper.open_browser()

    def picture_step(self):
        if self.upload:
            self.upload_multiple_pictures(self.pictures)

    def unfollow_users_step(self, users_to_unfollow=None):
        if users_to_unfollow:
            self.unfollow_multiple_users(users_to_unfollow)

    def explore_tags(self):
        """
        Start the real step.

        1. Search by hashtags

        """
        self.explore_tags_by_multiple_hashtags(
            self.search_tags,
            min_followers=self.min_followers_for_a_new_follow,
            total_to_follow=self.total_to_follow_per_hashtag,
            ignore_users=self.ignore_users,
            posts_per_hashtag=self.posts_per_hashtag,
            ignore_tags=self.ignore_tags
        )

    def run(self, users_to_unfollow=None, users_following=None):
        """
        :type users_to_unfollow: iter(Follower)
        :type users_following: iter(Follower)

        1. login
        2. pics
        3. unfollow users
        4. follow process
            per post
            me gusta
            comment probability
            follow probability
        """
        self.start_browser()
        self.login()
        self.picture_step()
        self.unfollow_users_step(users_to_unfollow=users_to_unfollow)

        # set the users that are already followed
        if users_following:
            self.users_following_to_ignore = users_following
        self.explore_tags()
