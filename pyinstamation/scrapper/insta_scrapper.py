import logging

from .base import BaseScrapper

from . import instagram_const


logger = logging.getLogger(__name__)


class InstaScrapper(BaseScrapper):

    def login(self, username, password):
        logger.info('[LOGIN] Starting...')
        self.find('xpath', instagram_const.LOGIN_LINK, wait=False).click()

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

    def upload_picture(self, image_path, comment):
        print('uploading picture...', image_path)

        # simulate the click in the Camera Logo
        image_input = self.find('class_name', instagram_const.UPLOAD_PICTURE_CAMARA_CSS_CLASS)
        image_input.click()
        # image_input = self.browser.find_element_by_class_name(instagram_const.UPLOAD_PICTURE_CAMARA_CSS_CLASS).click()
        # self.wait(5)

        image_input = self.browser.find_element_by_xpath(instagram_const.UPLOAD_PICTURE_INPUT_FILE)
        image_input.send_keys(image_path)

        self.wait_explicit()
        self.browser.find_element_by_xpath(instagram_const.UPLOAD_PICTURE_NEXT_LINK).click()

        # Set the comment
        self.wait_explicit(seconds=6)
        comment_input = self.browser.find_element_by_xpath(instagram_const.UPLOAD_PICTURE_TEXTAREA_COMMENT)
        comment_input.click()

        self.wait_explicit()
        comment_input.send_keys(comment)

        self.wait_explicit()
        self.browser.find_element_by_xpath(instagram_const.UPLOAD_PICTURE_SHARE_LINK).click()

    def get_user_page(self, username):
        url = "{0}/{1}".format(self.website_url, username)
        self.browser.get(url)

    def follow_user(self, username):
        """Follows a given user."""
        return self._follow_unfollow_process(username)

    def unfollow_user(self, username):
        return self._follow_unfollow_process(username, follow_user=False)

    def _follow_unfollow_process(self, username, follow_user=True):
        """
        By default try to follow the user
        """
        self.get_user_page(username)
        follow_button = self.browser.find_element_by_xpath(
            instagram_const.FOLLOW_UNFOLLOW_BUTTON)

        self.wait_explicit(seconds=10)

        if follow_user:
            if follow_button.text == instagram_const.FOLLOW_BUTTON_TEXT:
                follow_button.click()
                print('---> Now following: {}'.format(username))
                self.wait_explicit(seconds=3)
                return True

            print('---> {} is already followed'.format(username))
            self.wait_explicit(seconds=10)
            return False

        # try to unfollow the suer
        if follow_button.text == 'Following':
            follow_button.click()
            print('---> Now Unfollowing: {}'.format(username))
            self.wait_explicit(seconds=3)
            return True

        print('---> {} is already Unfollowed'.format(username))
        self.wait_explicit(seconds=10)
        return False
