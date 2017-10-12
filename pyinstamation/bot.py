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


class InstaBot:

    def __init__(self, scrapper, username=None, password=None, is_new=True):
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
        self.likes_enabled = _posts.get('likes_enabled', True)
        self.likes_per_day = _posts.get('likes_per_day', 0)
        self.like_probability = _posts.get('like_probability', 0.5)
        self.comments_per_day = _posts.get('comments_per_day', 0)
        self.comment_enabled = _posts.get('comment_enabled', False)
        self.comment_generator = _posts.get('comment_generator', False)
        self.comment_probability = _posts.get('comment_probability', 0.5)
        self.search_tags = self.remove_hashtags(_posts.get('search_tags', []))
        self.custom_comments = _posts.get('custom_comments', [])
        self.ignore_tags = self.remove_hashtags(_posts.get('ignore_tags', []))
        self.posts_per_day = _posts.get('posts_per_day', None)
        self.posts_per_hashtag = _posts.get('posts_per_hashtag', None)

        _followers = CONFIG.get('followers', {})
        self.ignore_users = _followers.get('ignore_users', [])
        self.follow_enable = _followers.get('follow_enable', False)
        self.min_followers = _followers.get('min_followers', 100)
        self.max_followers = _followers.get('max_followers', 7000)
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
        self.posts_explored = 0
        self.commented_post = 0
        self.total_followers = 0
        self.total_following = 0
        self.likes_given_by_bot = 0
        self.unlikes_given_by_bot = 0
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
    def remove_hashtags(tags):
        return list(map(lambda x: x.replace('#', ''), tags))

    @staticmethod
    def probability_of_occurrence(probability):
        """
        :type threshold: float
        """
        probability = float(probability)
        r = random.uniform(0, 1)
        is_lower = r <= probability
        msg = 'Random ({0:.2}) ' + 'not ' * (not is_lower) + 'lower than probability ({1:.2})'
        logger.info(msg.format(r, probability))
        return is_lower

    def start_browser(self):
        self.scrapper.open_browser()

    def login(self):
        if self.scrapper.login(self.username, self.password):
            self._user_login = True

    def logout(self):
        if self.user_login:
            self.scrapper.logout()
        else:
            logger.debug('Not logged in')

        self.scrapper.close_browser()
        self._user_login = False  # always set user not logged
        return True

    def stop(self):
        return self.logout()

    @property
    def user_login(self):
        return self._user_login

    def user_info(self, username):
        if self._user_login:
            return self.scrapper.user_info(username)
        return {}

    def my_profile_info(self):
        if self._user_login:
            my_profile = self.user_info(self.username)
            self.total_followers = my_profile.get('total_followers')
            self.total_following = my_profile.get('total_following')

    def upload_picture(self, image_path, description=None):
        self.scrapper.upload_picture(image_path, description)
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
            descripton = picture.get('descripton', None)
            self.upload_picture(pic, descripton)

    def follow(self, username, conditions_checked=True, min_followers=None,
               max_followers=None):
        if self.user_login:

            if not conditions_checked:
                if not self._should_follow(username):
                    return False

            if self.scrapper.follow(username):
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

    def follow_multiple_users(self, username_list, min_followers=None,
                              max_followers=None):
        for username in username_list:
            self.follow(
                username,
                conditions_checked=False,
                min_followers=min_followers,
                max_followers=max_followers
            )

    def unfollow(self, username):
        if self.user_login:
            if self.scrapper.unfollow(username):
                self.users_unfollowed_by_bot.append(
                    FollowedUser(username=username, follow_date=datetime.utcnow())
                )
                self.total_following -= 1
                return True
        return False

    def unfollow_multiple_users(self, users_list):
        """
        :type user_list: iter(Followers)
        """
        for user in users_list:
            self.unfollow(user.username)

    def like(self, post_link):
        if self.user_login:
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

    def comment_issuer(self):
        comment = None
        if self.comment_generator:
            comment = comments.generate_comment()
        elif self.custom_comments:
            comment = random.choice(self.custom_comments)
        return comment

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
            comment = post_object.get('comment', default_comment)

            if not post or not comment:
                continue

            self.comment(post, comment)

        total_comments_made = self.commented_post - current_commented_posts
        logger.info('Commented {0} of {1}'.format(total_comments_made, len(posts_list)))

    def _should_follow(self, username, ignore_users=None):
        min_followers = self.min_followers
        max_followers = self.max_followers

        if not self.follow_enable:
            return False

        if not self.total_user_followed_by_bot < self.follow_per_day:
            logger.info('Follows per day exceeded.')
            self.follow_enable = False
            return False

        if min_followers or max_followers:
            if min_followers is None:
                min_followers = 0
            if max_followers is None:
                max_followers = 1 << 32
            user_info = self.user_info(username)
            user_followers = user_info.get('total_followers', 0)

            if not (min_followers <= user_followers <= max_followers):
                msg = '{username} not in range of followers min ({min_fs}) and max ({max_fs})'
                logger.info(msg.format(username=username, min_fs=min_followers,
                                       max_fs=max_followers))
                return False

        if ignore_users and username in ignore_users:
            logger.info('ignoring user {username}'.format(username=username))
            return False

        return self.probability_of_occurrence(self.follow_probability)

    def _should_like(self):
        if not self.likes_enabled:
            return False

        if not self.likes_given_by_bot < self.likes_per_day:
            logger.info('Likes per day exceeded.')
            self.likes_enabled = False
            return False

        return self.probability_of_occurrence(self.like_probability)

    def _should_comment(self):
        if not self.comment_enabled:
            return False

        if self.comments_per_day <= self.commented_post:
            logger.info('Comments per day exceeded.')
            self.comment_enabled = False
            return False

        return self.probability_of_occurrence(self.comment_probability)

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

    def _ignore_followed(self, username):
        return any(user.username == username for user in
                   self.users_following_to_ignore)

    def explore_hashtag(self, hashtag,
                        total_to_follow=1, ignore_users=None,
                        posts_per_hashtag=None, ignore_tags=None):

        self.scrapper.get_hashtag_page(hashtag)
        posts = self.scrapper.get_posts_by_hashtag(hashtag)

        if not posts:
            logger.info('No posts were found for HASHTAG "{0}"'.format(hashtag))
            return 0

        users_followed_by_hashtag = 0
        posts_analyzed = 0
        for i, post in enumerate(posts):

            # if the goal was reached, finish.
            if not self._should_explore_tags:
                break

            if posts_per_hashtag and posts_per_hashtag <= i:
                return posts_analyzed

            # if there is a post there is a code....
            post_code = post.get('code')
            post_url = self.scrapper.generate_post_link_by_code(post_code)
            logger.info('Current post: {0}'.format(post_url))
            if not self._validate_post(post, ignore_tags=ignore_tags):
                msg = 'Ignoring post "{0}". Has at least one hashtag of "{1}"'
                logger.info(msg.format(post_url, ignore_tags))
                continue

            if self.posts_per_day:
                logger.info('Post {0}/{1}'.format(self.posts_explored, self.posts_per_day))
            self.scrapper.wait(sleep_time=3)
            username = self.scrapper.username_in_post_page(post_url)
            if username is None:
                continue

            if self._ignore_followed(username):
                msg = 'Skip. Already following the user "{0}"'.format(username)
                logger.debug(msg)
                continue

            self.posts_explored += 1

            if self._should_like():
                self.like(post_url)

            if self._should_comment():
                comment = self.comment_issuer()

                if comment:
                    self.comment(post_url, comment)
                    logger.info('Comment: "{0}"'.format(comment))

            if self._should_follow(username, ignore_users=ignore_users):
                if self.follow(username):
                    logger.info('Followed: "{0}"'.format(username))
                    users_followed_by_hashtag += 1

            posts_analyzed += 1

        return posts_analyzed

    @property
    def _should_explore_tags(self):
        if (self.posts_per_day is not None) and self.posts_explored >= self.posts_per_day:
            return False

        return (self.likes_given_by_bot <= self.likes_per_day or
                self.commented_post <= self.comments_per_day or
                self.total_user_followed_by_bot <= self.follow_per_day)

    def explore_hashtags(self):
        total_to_follow = self.follow_per_day
        ignore_users = self.ignore_users
        posts_per_hashtag = self.posts_per_hashtag
        ignore_tags = self.ignore_tags
        hashtags = self.search_tags

        total = 0

        while self._should_explore_tags:
            for tag in hashtags:
                hashtag_name = tag

                if isinstance(tag, dict):
                    hashtag_name = tag.get('hashtag')
                    total_to_follow = tag.get('total_to_follow', total_to_follow)

                logger.info('Processing hashtag "{0}"'.format(hashtag_name))

                total += self.explore_hashtag(
                    hashtag_name,
                    total_to_follow=total_to_follow,
                    ignore_users=ignore_users,
                    posts_per_hashtag=posts_per_hashtag,
                    ignore_tags=ignore_tags
                )

                if not self._should_explore_tags:
                    break

        return total

    def picture_step(self):
        if self.upload:
            self.upload_multiple_pictures(self.pictures)

    def unfollow_users_step(self, users_to_unfollow=None):
        if users_to_unfollow:
            self.unfollow_multiple_users(users_to_unfollow)

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
        try:
            self.start_browser()
            self.login()
            self.picture_step()
            self.unfollow_users_step(users_to_unfollow=users_to_unfollow)

            # set the users that are already followed
            if users_following:
                self.users_following_to_ignore = users_following
            self.explore_hashtags()
        except Exception as e:
            logger.exception('Something happened. Tracking to fix')
        finally:
            self.stop()
