import os
import sys
import yaml
import logging

from scrapper.insta_scrapper import InstaScrapper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_TEST_PATH = os.path.join(BASE_DIR, 'scrapper', 'chiche.jpg')

logger = logging.getLogger(__name__)


class InstaBot:

    # urls
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    # LOGIN_URL = '{0}{1}'.format(BASE_URL, '/accounts/login/ajax/')
    # https://www.instagram.com/accounts/login/ajax/?hl=es
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'

    # settings
    USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    ACCEPT_LANGUAGE = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    SLEEP_TIME = 3

    def __init__(self, scrapper, username, password):
        self.username = username
        self.password = password
        self.scrapper = scrapper
        self._user_login = False
        self.followers = 0
        self.following = 0

        self._configure_log()
        self._reach_website()

    def _reach_website(self):
        self.scrapper.reach_website()

    def _configure_log(self):
        logger.info('Iniciando bot....')

    def login(self):
        if self.scrapper.login(self.username, self.password):
            self._user_login = True

    def logout(self):
        if self.user_login:
            self.scrapper.logout()
        else:
            logger.info('login first alsjeblieft')

    @property
    def user_login(self):
        return self._user_login

    def upload_picture(self, image_path, comment):
        self.scrapper.upload_picture(image_path, comment)

    def start(self):
        pass

    def comment(self):
        pass

    def follow_user(self, username):
        if self._user_login:
            if self.scrapper.follow_user(username):
                self.following += 1

    def unfollow_user(self, username):
        if self._user_login:
            if self.scrapper.unfollow_user(username):
                self.following -= 1

    def follow_multipleuser(self, username_list):
        for username in username_list:
            self.follow_user(username)

    def unfollow_multipleuser(self, username_list):
        for username in username_list:
            self.unfollow_user(username)


if __name__ == '__main__':
    with open("config.yaml", 'r') as stream:
        try:
            CONFIG = yaml.load(stream)
        except yaml.YAMLError as exc:
            sys.exit(exc)

    scrapper = InstaScrapper(CONFIG.get('site_url'))
    bot = InstaBot(scrapper, CONFIG.get('username'), CONFIG.get('password'))

    # actions
    bot.login()
    # bot.follow_user('woile')
    # bot.follow_multipleuser(['woile', 'marcosschroh'])
    # bot.unfollow_user('woile')
    # bot.unfollow_multipleuser(['woile', 'marcosschroh'])
    # bot.upload_picture(IMAGE_TEST_PATH, '#chiche #bombom #pp')
