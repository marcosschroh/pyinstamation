import datetime
from pyinstamation import FollowedUser
from pyinstamation.models import User, Follower
from pyinstamation.controller import Controller
from tests import DBTestCase


class MockUpBot:

    def __init__(self):
        self.users_followed_by_bot = 1
        self.users_unfollowed_by_bot = 1
        self.likes_given_by_bot = 1
        self.commented_post = 1
        self.users_followed_by_bot = [
            FollowedUser('mock_juan', datetime.datetime.now()),
            FollowedUser('mock_pepe', datetime.datetime.now()),
            FollowedUser('mock_pipo', datetime.datetime.now()),
        ]
        self.users_unfollowed_by_bot = [
            FollowedUser('mock_juan_unf', datetime.datetime.now()),
            FollowedUser('mock_pepe_unf', datetime.datetime.now()),
            FollowedUser('mock_pipo_unf', datetime.datetime.now()),
        ]

    def run(self, users_to_unfollow=None, users_following=None):
        return


class ControllerTest(DBTestCase):

    def setUp(self):
        self.user = User.create(username='darude')
        self.followers = ['user1', 'user2', 'user3']
        self.bot = MockUpBot()

        for username in self.followers:
            Follower.create(user=self.user, username=username)

    def test_controller_create_user(self):
        c = Controller(username='pepe')
        self.assertEqual(c.user.username, 'pepe')
        self.assertTrue(c.is_new)

    def test_controller_exists_user(self):
        c = Controller(username='darude')
        self.assertEqual(c.user.username, 'darude')
        self.assertFalse(c.is_new)

    def test_get_users_to_unfollow(self):
        c = Controller(username='pepe')
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        Follower.create(user=c.user, username='fulanito',
                        unfollow_date=yesterday)
        Follower.create(user=c.user, username='noUnfoll',
                        following=False, unfollow_date=yesterday)

        users = c.get_users_to_unfollow()
        self.assertEqual(users.count(), 1)

    def test_set_users_followed(self):
        followed = [
            FollowedUser('juan', datetime.datetime.now()),
            FollowedUser('miguel', datetime.datetime.now()),
            FollowedUser('arturo', datetime.datetime.now())
        ]
        c = Controller(username='pepe')
        c.set_users_followed(followed)
        total_followed = c.user.follower_set.select().count()
        self.assertEqual(total_followed, 3)

    def test_set_user_stats(self):
        c = Controller(username='pepe')
        c.set_user_stats(likes=4, comments=3, followed=2, unfollowed=1)
        self.assertEqual(c.user.likes, 4)
        self.assertEqual(c.user.commented, 3)
        self.assertEqual(c.user.followed, 2)
        self.assertEqual(c.user.unfollowed, 1)

    def test_set_users_unfollowed(self):
        c = Controller(username='pepe')
        unfollowed = [
            FollowedUser('user1', None),
            FollowedUser('user2', None),
            FollowedUser('user3', None)
        ]
        c.set_users_unfollowed(unfollowed)
        not_follows = c.user.follower_set.select(Follower.following == False)  # noqa
        self.assertEqual(not_follows.count(), 0)

    def test_get_users_following(self):
        c = Controller(username='darude')
        following = c.get_users_following()
        self.assertEqual(len(following), 3)

    def test_set_stats(self):
        c = Controller(username='pepe')
        c.set_stats(self.bot)
        self.assertEqual(c.user.likes, self.bot.likes_given_by_bot)

    def test_run(self):
        c = Controller(username='pepe')
        c.run(self.bot)
        self.assertEqual(c.user.likes, self.bot.likes_given_by_bot)
