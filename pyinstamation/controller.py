from .models import User, Follower
from pyinstamation import CONFIG
from pyinstamation.bot import InstaBot


class Controller:

    def __init__(self, username):
        user = User.get_or_create(username=username)
        self.user = user

    def get_users_to_follow(self):
        pass

    def get_users_to_unfollow(self):
        pass
