from pyinstamation import CONFIG
from pyinstamation.bot import InstaBot
from pyinstamation.controller import Controller


def parse_args():
    pass


if __name__ == '__main__':
    print("running nain")
    bot = InstaBot(CONFIG.get('username'), CONFIG.get('password'))

    # actions
    bot.login()
    # bot.follow
    # bot.follow_user('woile')
    # bot.follow_multiple_users(['woile', 'marcosschroh'])
    # bot.unfollow_user('woile')
    # bot.unfollow_multiple_users(['woile', 'marcosschroh'])
    # bot.upload_picture(IMAGE_TEST_PATH, '#chiche #bombom #pp')
