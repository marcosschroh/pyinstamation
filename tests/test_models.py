import datetime
import peewee
from pyinstamation.models import User, Follower, Statistics, future_rand_date
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

    def test_statistics_multiple_ok(self):
        stat = Statistics.create(
            user=self.user,
            likes=1,
            followed=1,
            unfollowed=1,
            commented=1
        )
        stat2 = Statistics.create(
            user=self.user,
            likes=2,
            followed=3,
            unfollowed=5,
            commented=4
        )
        stat3 = Statistics.create(
            user=self.user,
            likes=2,
            followed=3,
            unfollowed=4,
            commented=5
        )
        self.assertNotEqual(stat.timestamp, stat2.timestamp)
        self.assertNotEqual(stat2.timestamp, stat3.timestamp)
        self.assertEqual(Statistics.select.count(), 3)
