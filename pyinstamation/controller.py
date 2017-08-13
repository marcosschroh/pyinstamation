import peewee
from pyinstamation.models import User, Follower, future_rand_date
from pyinstamation import CONFIG
from pyinstamation.bot import InstaBot


class Controller:

    def __init__(self, username):
        user, is_new = User.get_or_create(username=username)
        self.user = user
        self.is_new = is_new

    def set_users_followed(self, users):
        """
        :type users: list(namedtuple)
        """
        assert type(users) is list, 'users is not a list'
        for user in users:
            unfollow_date = future_rand_date(date=user.followed_date)
            try:
                Follower.create(user=self.user, username=user.username, unfollow_date=unfollow_date)
            except peewee.IntegrityError:
                pass

    def get_users_to_unfollow(self):
        pass
