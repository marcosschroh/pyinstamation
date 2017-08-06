import time
import requests
import random


class Bot:

    # urls
    BASE_URL = 'https://www.instagram.com'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    LOGIN_URL = '{0}{1}'.format(BASE_URL, '/accounts/login/ajax/')
    # https://www.instagram.com/accounts/login/ajax/?hl=es
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'

    # settings
    USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    ACCEPT_LANGUAGE = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    SLEEP_TIME = 3

    # response code
    HTTP_200_OK = 200


    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.USER_AGENT,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })

        session.cookies.update({
            'sessionid': '',
            'mid': '',
            'ig_pr': '1',
            'ig_vw': '1920',
            'csrftoken': '',
            's_network': '',
            'ds_user_id': ''
        })

        r = session.get(self.BASE_URL)

        time.sleep(5 * random.random())

        # update session for next use
        csrftoken = r.cookies.get('csrftoken')
        session.headers.update({'X-CSRFToken': csrftoken})

        return session

    def _update_csrf(self, response):
        """
        Update the Session instance with the new csrftoken
        """
        csrftoken = response.cookies.get('csrftoken')
        self.session.headers.update({'X-CSRFToken': csrftoken})

    def login(self):

        data = {
            'username': self.username,
            'password': self.password
        }

        login_response = self.session.post(self.LOGIN_URL, data=data, allow_redirects=True)

        if login_response.status_code == self.HTTP_200_OK:
            print('Welkome... in DUTCH %s', % (self.username))
            self._update_csrf(login_response)
            time.sleep(self.SLEEP_TIME * random.random())
        else:
            print('Wrong username or password...')

    def logout(self):
        pass

    def follow(self, user_id):
        pass

    def unfollow(self, user_id):
        pass