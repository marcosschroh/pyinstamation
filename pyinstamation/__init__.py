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
