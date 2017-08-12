import sys
import yaml
import logging
import logging.config

from pyinstamation.scrapper.insta_scrapper import InstaScrapper
from pyinstamation.bot import InstaBot


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s][%(name)s.%(funcName)s:%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file_handler': {
            'level': 'ERROR',
            'filename': '/tmp/api.log',
            'class': 'logging.FileHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'pyinstamation': {
            'handlers': ['default', 'file_handler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING)


CONFIG = {}


def load_config():
    global CONFIG

    if CONFIG:
        return
    with open('./config.yaml', 'r') as stream:
        try:
            CONFIG = yaml.load(stream)
        except yaml.YAMLError as exc:
            sys.exit(exc)


load_config()
scrapper = InstaScrapper(CONFIG.get('site_url'))
bot = InstaBot(scrapper, CONFIG.get('username'), CONFIG.get('password'))

# actions
bot.login()
# bot.follow
# bot.follow_user('woile')
# bot.follow_multiple_users(['woile', 'marcosschroh'])
# bot.unfollow_user('woile')
# bot.unfollow_multiple_users(['woile', 'marcosschroh'])
# bot.upload_picture(IMAGE_TEST_PATH, '#chiche #bombom #pp')
# bot.like_post('https://www.instagram.com/p/BXamBMihdBF/')
# bot.unlike_post('https://www.instagram.com/p/BXamBMihdBF/')
