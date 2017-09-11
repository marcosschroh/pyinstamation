import os
import logging
import requests

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base import BaseScrapper

from . import instagram_const as const
from .utils import save_page_source


logger = logging.getLogger(__name__)


class InstaScrapper(BaseScrapper):

    def login(self, username, password):
        self.get_page(const.URL_LOGIN)
        logger.debug('Attempting to login user "%s"', username)

        username_input = self.find('xpath', const.LOGIN_INPUT_USERNAME, wait=False)
        password_input = self.find('xpath', const.LOGIN_INPUT_PASSWORD, wait=False)

        username_input.send_keys(username)
        password_input.send_keys(password)
        self.wait()
        self.browser.find_element_by_xpath(const.LOGIN_BUTTON).click()

        WebDriverWait(self.browser, 5).until(
            lambda _: self.browser.get_cookie('sessionid'))
        logger.info('Login successful. Username "%s"', username)
        return bool(self.browser.get_cookie('sessionid'))

    def logout(self):
        logger.info('Logout done.')
        # TODO: Log out user
        return True

    def user_page(self, username):
        url = const.URL_USER_DETAIL.format(username, '')
        self.get_page(url)

    def user_info(self, username):
        url = os.path.join(const.HOSTNAME,
                           const.URL_USER_DETAIL.format(username, '?__a=1'))
        # get the response
        r = requests.get(url)
        user = {}

        if r.ok:
            # parse json
            json_content = r.json()
            save_page_source(const.URL_USER_DETAIL.format(username, '?__a=1'),
                             json_content)
            user = json_content.get('user', {})

        return {
            'total_followers': user.get('followed_by', {}).get('count', 0),
            'total_following': user.get('follows', {}).get('count', 0)
        }

    def user_info_in_post_page(self, username):
        self.user_page(username)

        total_following = self.find(
            'xpath', const.USER_FOLLOWING.format(username)).text

        total_followers = self.find(
            'xpath', const.USER_FOLLOWERS.format(username)).text

        # Maybe we should check that it can be cast to int...
        total_following = int(total_following)
        total_followers = int(total_followers)

        # TODO: get friends/following list

        return {
            'total_followers': total_followers,
            'total_following': total_following,
        }

    def _select_image(self, image_path):
        """Click on the camera logo is required in order to work."""
        image_input = self.find('class_name', const.UPLOAD_PICTURE_CAMARA_CLASS)
        image_input.click()
        image_input = self.find('xpath', const.UPLOAD_PICTURE_INPUT_FILE,
                                wait=False)
        image_input.send_keys(image_path)
        save_page_source(self.current_url.path, self.page_source)
        return True

    def _format_image(self):
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH, const.UPLOAD_PICTURE_NEXT_LINK)))
        element.click()
        save_page_source(self.current_url.path, self.page_source)
        return True

    def _add_description(self, description=None):
        if description is None:
            return False
        comment_input = self.find('xpath',
                                  const.UPLOAD_PICTURE_TEXTAREA_COMMENT)
        comment_input.click()
        save_page_source(self.current_url.path, self.page_source)
        comment_input.send_keys(description)
        self.wait(explicit=True)
        return True

    def _share_image(self):
        self.browser.find_element_by_xpath(const.UPLOAD_PICTURE_SHARE_LINK).click()
        save_page_source(self.current_url.path, self.page_source)
        return True

    def upload_picture(self, image_path, description=None):
        logger.debug('Picture to upload: %s', image_path)
        self._select_image(image_path)
        self._format_image()
        self._add_description(description)
        self._share_image()
        logger.info('Upload successful. Picture: %s', image_path)
        return True

    @property
    def _is_followed(self):
        """Use only after getting a post page somewhere else."""
        button = self.find('xpath', const.FOLLOW_UNFOLLOW_BUTTON, wait=False)
        return button.text == 'Following'

    def _click_follow_button(self):
        follow_button = self.find('xpath', const.FOLLOW_UNFOLLOW_BUTTON)
        follow_button.click()

    def _validate_follow_click(self, operation):
        _text = {
            'follow': 'Following',
            'unfollow': 'Follow'
        }
        self.wait(explicit=True)
        self.browser.refresh()
        element = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH, const.FOLLOW_UNFOLLOW_BUTTON)))

        return element.text == _text[operation]

    def follow(self, username):
        self.user_page(username)

        if self._is_followed:
            logger.debug('Already followed "%s"', username)
            return False
        self._click_follow_button()

        is_ok = self._validate_follow_click(operation='follow')
        if not is_ok:
            msg = 'Could not follow "%s", instagram may be blocking'
            logger.info(msg, username)
            return False

        logger.info('Following user "%s"', username)
        return True

    def unfollow(self, username):
        self.user_page(username)

        if not self._is_followed:
            logger.debug('Already unfollowed "%s"', username)
            return False
        self._click_follow_button()

        is_ok = self._validate_follow_click(operation='unfollow')
        if not is_ok:
            msg = 'Could not unfollow "%s", instagram may be blocking'
            logger.info(msg, username)
            return False

        logger.info('Unfollowed user "%s"', username)
        return True

    @property
    def _is_liked(self):
        """Use only after getting a post page somewhere else."""
        e = self.find('xpath', const.LIKE_UNLIKE_BUTTON, wait=False)
        return e.text == 'Unlike'

    def _click_heart_button(self):
        """Use only after getting a post page somewhere else."""
        button = self.find('xpath', const.LIKE_UNLIKE_BUTTON)
        button.click()

    def like(self, post_link):
        self.get_page(post_link)

        if self._is_liked:
            logger.debug('Already liked: "%s"', post_link)
            return False

        self._click_heart_button()
        logger.info('Liked: "%s"', post_link)
        return True

    def unlike(self, post_link):
        self.get_page(post_link)

        if not self._is_liked:
            logger.debug('Already unliked: "%s"', post_link)
            return False

        self._click_heart_button()
        logger.info('Unliked: "%s"', post_link)
        return True

    def comment(self, post_link, comment):
        logger.info('Attempting comment at post: %s', post_link)

        self.get_page(post_link)

        new_comment_btn = self.find('xpath', const.REQUEST_NEW_COMMENT_BUTTON)
        new_comment_btn.click()
        save_page_source(self.current_url.path, self.page_source)
        self.wait(explicit=True)

        textarea_comment = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH, const.COMMENT_TEXTEAREA)))
        textarea_comment.send_keys(comment)
        self.wait(explicit=True)

        send_comment_button = self.find('xpath', const.SEND_COMMENT_BUTTON)
        send_comment_button.click()
        self.wait(explicit=True)

        logger.info('Post commented: %s', post_link)

        return True

    def username_in_post_page(self, post_url):
        self.get_page(post_url)
        web_element = self.find('xpath', const.USERNAME_IN_POST_PAGE)
        user_page_link = web_element.get_attribute('href')

        # we expect always a format like.. 'https://www.instagram.com/voetbal_in_haarlem/'
        return user_page_link.split('/')[-2]

    def generate_post_link_by_code(self, post_code):
        return const.URL_MEDIA_DETAIL.format(post_code, '')

    def get_hashtag_page(self, hashtag):
        url = const.URL_TAG.format(hashtag, '')
        self.get_page(url, sleep_time=5)

    def get_posts_by_hashtag(self, hashtag):
        url = os.path.join(const.HOSTNAME, const.URL_TAG.format(hashtag, '?__a=1'))
        # get the response
        r = requests.get(url)
        if r.ok:
            json_content = r.json()
            save_page_source(const.URL_TAG.format(hashtag, '?__a=1'), json_content)
            return json_content.get('tag', {}).get('media', {}).get('nodes', [])
        return []
