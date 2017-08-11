from scrapper.base import BaseScrapper

from scrapper import instagram_const


class InstaScrapper(BaseScrapper):

    def login(self, username, password):
        self.browser.find_element_by_xpath(instagram_const.LOGIN_LINK).click()
        self.wait(2)

        username_input = self.browser.find_element_by_xpath(instagram_const.LOGIN_INPUT_USERNAME)
        password_input = self.browser.find_element_by_xpath(instagram_const.LOGIN_INPUT_PASSWORD)

        username_input.send_keys(username)
        self.wait_explicit()
        password_input.send_keys(password)

        self.browser.implicitly_wait(self.SLEEP_TIME)
        self.browser.find_element_by_xpath(instagram_const.LOGIN_BUTTON).click()

        print('Welkome... {0}'.format(username))

        self.wait_explicit(10)

        if self.browser.get_cookie('sessionid'):
            return True
        return False

    def logout(self):
        self._close_browser()

    def upload_picture(self, image_path, comment):
        print('uploading picture...', image_path)

        # simulate the click in the Camera Logo
        image_input = self.browser.find_element_by_class_name(instagram_const.UPLOAD_PICTURE_CAMARA_CSS_CLASS).click()
        self.wait(5)

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
