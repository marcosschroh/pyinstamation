import os

from scrapper.base import InstaScrapper

BASE_URL = 'https://www.instagram.com'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_TEST_PATH = os.path.join(BASE_DIR, 'scrapper', 'chiche.jpg')


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

    def start(self):
        self.init_scraping()
        self.login()

    def init_scraping(self):
        self.scrapper.reach_website()

    def login(self):
        self.scrapper.login(self.username, self.password)

    def logout(self):
        self.scrapper.logout()

    def upload_picture(self, image_path):
        self.scrapper.upload_picture(image_path)

    def comment(self):
        pass

    def follow(self, user_id):
        pass

    def unfollow(self, user_id):
        pass


if __name__ == '__main__':
    scrapper = InstaScrapper(BASE_URL)
    bot = InstaBot(scrapper, 'discovrar', 'discorvd')
    bot.start()

    bot.upload_picture(IMAGE_TEST_PATH)
