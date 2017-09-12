#!/usr/bin/env python
import sys
import os  # noqa
sys.path.append('../pyinstamation')

from pyinstamation.bot import InstaBot  # noqa
from pyinstamation.scrapper import InstaScrapper  # noqa
from pyinstamation import config  # noqa


FILEPATH = os.path.abspath('tests/static/one_day.jpg')

NOT_FOLLOWED_USER = {
    'user': 'fancyhoustonapartments',
    'post_to_like_state': 'BY3rdjrH-cr',
    'post_to_unlike_state': 'BY3Bg4THwNi'
}

FOLLOWED_USER = {
    'user': 'celine_legallic',
    'post_to_like_state': 'BYxjRwQAq6N',
    'post_to_unlike_state': 'BYu8NnXAPow'
}

TAGS = ['apartmentdecor', 'architecture']


def to_like(bot, post_id):
    post_link = bot.scrapper.generate_post_link_by_code(post_id)
    bot.scrapper.get_page(post_link)
    if bot.scrapper._is_liked:
        bot.unlike(post_link)
        bot.scrapper.get_page(post_link)


def to_unlike(bot, post_id):
    post_link = bot.scrapper.generate_post_link_by_code(post_id)
    bot.scrapper.get_page(post_link)
    if not bot.scrapper._is_liked:
        bot.like(post_link)
        bot.scrapper.get_page(post_link)


config.load_config(filepath='test.config.yaml')
config.SAVE_SOURCE = True

s = InstaScrapper()
bot = InstaBot(s)

bot.start_browser()
bot.login()
bot.upload_picture(FILEPATH, description='New pic next time\n#motivation #go')
bot.scrapper.get_page('/')
bot.my_profile_info()
bot.scrapper.user_info_in_post_page(bot.username)

to_like(bot, NOT_FOLLOWED_USER['post_to_like_state'])
to_unlike(bot, NOT_FOLLOWED_USER['post_to_unlike_state'])

to_like(bot, FOLLOWED_USER['post_to_like_state'])
to_unlike(bot, FOLLOWED_USER['post_to_unlike_state'])
bot.comment(NOT_FOLLOWED_USER['post_to_like_state'], 'wow!')

bot.scrapper.user_page(NOT_FOLLOWED_USER['user'])
if bot.scrapper._is_followed:
    bot.unfollow(NOT_FOLLOWED_USER['user'])
    bot.scrapper.user_page(NOT_FOLLOWED_USER['user'])

bot.scrapper.user_page(FOLLOWED_USER['user'])
if not bot.scrapper._is_followed:
    bot.follow(FOLLOWED_USER['user'])
    bot.scrapper.user_page(FOLLOWED_USER['user'])

for tag in TAGS:
    bot.scrapper.get_hashtag_page(tag)
    bot.scrapper.get_posts_by_hashtag(tag)

bot.logout()
