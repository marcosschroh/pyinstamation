import datetime
import peewee
from pyinstamation.models import User, Follower, future_rand_date
from tests import DBTestCase


class ModelTest(DBTestCase):

    def setUp(self):
        self.user = User.create(username='darude')
        self.followers = []
        for username in ['user1', 'user2', 'user3']:
            f = Follower.create(user=self.user, username=username)
            self.followers.append(f)

    def test_create_user(self):
        self.user = User.create(username='willy')
        user = User.get(User.username == 'willy')
        total_users = User.select().count()
        self.assertEqual(user.username, 'willy')
        self.assertEqual(total_users, 2)

    def test_has_followers(self):
        following = self.user.follower_set.select().count()
        self.assertEqual(following, 3)

    def test_future_rand_date(self):
        new_date = future_rand_date()
        self.assertIsInstance(new_date, datetime.datetime)

    def test_already_exist_username(self):
        with self.assertRaises(peewee.IntegrityError):
            User.create(username='darude')
