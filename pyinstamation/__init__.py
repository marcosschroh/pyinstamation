import sys
import yaml

from pyinstamation.scrapper.insta_scrapper import InstaScrapper
from pyinstamation.bot import InstaBot


with open('../config.yaml', 'r') as stream:
    try:
        CONFIG = yaml.load(stream)
    except yaml.YAMLError as exc:
        sys.exit(exc)

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
