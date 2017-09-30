"""Do not run this here, it won't work, it must be in the root project."""
from pyinstamation.bot import InstaBot
from pyinstamation.scrapper import InstaScrapper


POST_LINK = 'p/not_a_real_post_id'
USERNAME = 'not_a_real_username'
PASSWORD = 'not_a_real_password'

s = InstaScrapper()
bot = InstaBot(s, username=USERNAME, password=PASSWORD)

bot.start_browser()
bot.login()
bot.upload_picture('not/a/real/absolute/path', description='fake description')
bot.stop()
