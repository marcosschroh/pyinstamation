import unittest
import datetime
from pyinstamation import FollowedUser
from pyinstamation.models import User, Follower
from pyinstamation.controller import Controller
from tests import DBTestCase

# follow/unfollow -> follow someone, then unfollow after 2 or 3 days. random between
# findTrends
# schedule


class ControllerTest(DBTestCase):

    def setUp(self):
        self.user = User.create(username='darude')
        self.followers = ['user1', 'user2', 'user3']
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
        Follower.create(user=c.user, username='fulanito', unfollow_date=yesterday)
        Follower.create(user=c.user, username='noUnfoll', following=False, unfollow_date=yesterday)
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

    def test_set_stats(self):
        c = Controller(username='pepe')
        c.set_user_stats(likes=4, comments=3, followed=2, unfollowed=1)
        self.assertEqual(c.user.likes, 4)
        self.assertEqual(c.user.commented, 3)
        self.assertEqual(c.user.followed, 2)
        self.assertEqual(c.user.unfollowed, 1)

    def test_set_users_unfollowed(self):
        c = Controller(username='pepe')
        unfollowed = [
            FollowedUser('user1', datetime.datetime.now()),
            FollowedUser('user2', datetime.datetime.now()),
            FollowedUser('user3', datetime.datetime.now())
        ]
        c.set_users_unfollowed(unfollowed)
        assert c.user.follower_set.select(Follower.following==False).count() == 0



if __name__ == '__main__':
    unittest.main()
