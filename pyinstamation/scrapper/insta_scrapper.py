import logging
import requests

from selenium.common.exceptions import NoSuchElementException

from .base import BaseScrapper

from . import instagram_const


logger = logging.getLogger(__name__)


class InstaScrapper(BaseScrapper):

    # urls
    URL_TAG = 'https://www.instagram.com/explore/tags/{0}/{1}'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    # LOGIN_URL = '{0}{1}'.format(BASE_URL, '/accounts/login/ajax/')
    # https://www.instagram.com/accounts/login/ajax/?hl=es
    url_logout = 'https://www.instagram.com/accounts/logout/'
    URL_MEDIA_DETAIL = 'https://www.instagram.com/p/{0}/{1}'
    URL_USER_DETAIL = 'https://www.instagram.com/{0}/{1}'

    def login(self, username, password):
        logger.info('[LOGIN] Starting...')
        self.find('xpath', instagram_const.LOGIN_LINK).click()

        username_input = self.find('xpath', instagram_const.LOGIN_INPUT_USERNAME, wait=False)
        password_input = self.find('xpath', instagram_const.LOGIN_INPUT_PASSWORD, wait=False)

        username_input.send_keys(username)
        password_input.send_keys(password)
        self.wait()
        self.browser.find_element_by_xpath(instagram_const.LOGIN_BUTTON).click()
        self.wait(explicit=True)

        logger.info('[LOGIN] Success for user: %s', username)
        return bool(self.browser.get_cookie('sessionid'))

    def logout(self):
        self.close_browser()

    def get_user_info(self, username):
        url = self.URL_USER_DETAIL.format(username, '?__a=1')

        # get the response
        r = requests.get(url)
        user = {}

        if r.status_code.ok:
            # parse json
            json_content = r.json()
            user = json_content.get('user', {})

        return {
            'total_followers': user.get('followed_by', {}).get('count', 0),
            'total_following': user.get('follows', {}).get('count', 0)
        }

    def get_user_info_in_post_page(self, username):
        self.get_user_page(username)

        total_following = self.find(
            'xpath', instagram_const.USER_FOLLOWING.format(username)).text

        total_followers = self.find(
            'xpath', instagram_const.USER_FOLLOWERS.format(username)).text

        # Maybe we should check that it can be cast to int...
        total_following = int(total_following)
        total_followers = int(total_followers)

        # TODO: get friends/following list

        return {
            'total_following': total_following,
            'total_followers': total_followers,
        }

    def get_my_profile_page(self, my_username):
        self.get_user_page(my_username)

    def upload_picture(self, image_path, comment):
        logger.info('uploading picture...', image_path)

        # simulate the click in the Camera Logo
        image_input = self.find(
            'class_name', instagram_const.UPLOAD_PICTURE_CAMARA_CSS_CLASS)
        image_input.click()

        image_input = self.browser.find_element_by_xpath(
            instagram_const.UPLOAD_PICTURE_INPUT_FILE)
        image_input.send_keys(image_path)

        self.wait_explicit()
        self.browser.find_element_by_xpath(
            instagram_const.UPLOAD_PICTURE_NEXT_LINK).click()

        # Set the comment
        self.wait_explicit(seconds=6)
        comment_input = self.browser.find_element_by_xpath(
            instagram_const.UPLOAD_PICTURE_TEXTAREA_COMMENT)
        comment_input.click()

        self.wait_explicit()
        comment_input.send_keys(comment)

        self.wait_explicit()
        self.browser.find_element_by_xpath(
            instagram_const.UPLOAD_PICTURE_SHARE_LINK).click()

    def get_user_page(self, username):
        url = self.URL_USER_DETAIL.format(username, '')
        self.get_page(url)

    def follow_user(self, username, min_followers=None, max_followers=None):
        """Follows a given user."""
        return self._follow_unfollow_process(username)

    def unfollow_user(self, username):
        return self._follow_unfollow_process(username, follow_user=False)

    def _follow_unfollow_process(self, username, follow_user=True):
        """
        By default try to follow the user
        """
        self.get_user_page(username)
        
        follow_button = self.find(
            'xpath', instagram_const.FOLLOW_UNFOLLOW_BUTTON)

        if follow_user:
            if follow_button.text == instagram_const.FOLLOW_BUTTON_TEXT:
                
                follow_button.click()
                logger.info('---> Now following: {}'.format(username))
                self.wait_explicit(seconds=3)
                return True

            logger.info('---> {} is already followed'.format(username))
            self.wait_explicit(seconds=10)
            return False

        # try to unfollow the suer
        if follow_button.text == 'Following':
            follow_button.click()
            logger.info('---> Now Unfollowing: {}'.format(username))
            self.wait_explicit(seconds=3)
            return True

        logger.info('---> {} is already Unfollowed'.format(username))
        self.wait_explicit(seconds=10)
        return False

    def like_post(self, post_link):
        self._like_unlike_process(post_link)

    def unlike_post(self, post_link):
        self._like_unlike_process(post_link, like=False)

    def _like_unlike_process(self, post_link, like=True):
        """
        By default try to like a post.
        """
        self.get_page(post_link)

        button_text = instagram_const.UNLIKE_BUTTON_TEXT
        success_message = instagram_const.SUCCESS_UNLIKE_POST_MESSAGE
        fail_message = instagram_const.FAIL_UNLIKE_POST_MESSAGE

        if like:
            button_text = instagram_const.LIKE_BUTTON_TEXT
            success_message = instagram_const.SUCCESS_LIKE_POST_MESSAGE
            fail_message = instagram_const.FAIL_LIKE_POST_MESSAGE

        try:
            button = self.find('link_text', button_text, sleep_time=2)
            button.click()
            logger.info(success_message.format(post_link))
            self.wait_explicit(seconds=3)
            return True
        except NoSuchElementException:
            logger.info(fail_message.format(post_link))
            self.wait_explicit(seconds=3)
            return False

    def comment_post(self, post_link, comment):
        self.get_page(post_link)

        request_comment_button = self.find(
            'xpath', instagram_const.REQUEST_NEW_COMMENT_BUTTON)

        request_comment_button.click()
        self.wait_explicit(seconds=3)

        textarea_comment = self.find(
            'xpath', instagram_const.COMMENT_TEXTEAREA)
        textarea_comment.click()
        self.wait_explicit(seconds=3)

        textarea_comment.send_keys(comment)
        self.wait_explicit(seconds=5)

        send_comment_button = self.find(
            'xpath', instagram_const.SEND_COMMENT_BUTTON)
        send_comment_button.click()
        self.wait_explicit(seconds=3)

        logger.info('Now you has commend the {0} post with {1}'.format(post_link, comment))

        return True

    def get_username_in_post_page(self, post_url):
        self.get_page(post_url)
        web_element = self.find('xpath', instagram_const.USERNAME_IN_POST_PAGE)
        user_page_link = web_element.get_attribute('href')

        # we expect always a format like.. 'https://www.instagram.com/voetbal_in_haarlem/'
        return user_page_link.split('/')[-2]

    def generate_post_link_by_code(self, post_code):
        return self.URL_MEDIA_DETAIL.format(post_code, '')

    def get_hashtag_page(self, hashtag):
        url = self.URL_TAG.format(hashtag, '')
        self.get_page(url, sleep_time=5)

    def get_posts_by_hashtag(self, hashtag):
        url = self.URL_TAG.format(hashtag, '?__a=1')

        # get the response
        r = requests.get(url)

        if r.ok:
            # parse json
            json_content = r.json()
            return json_content.get('tag', {}).get('media', {}).get('nodes', [])
            # possible order
            # posts = sorted(n, key=lambda post: post.get('likes').get('count'))
        return []

    def find_by_hashtag(self, hashtag):
        self.get_hashtag_page(hashtag)
