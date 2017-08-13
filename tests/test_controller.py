import unittest
import datetime
from pyinstamation import FollowedUser
from pyinstamation.models import User, Follower
from pyinstamation.controller import Controller
from tests import DBTestCase


class ControllerTest(DBTestCase):

    def setUp(self):
        self.user = User.create(username='darude')
        self.followers = []
        for username in ['user1', 'user2', 'user3']:
            f = Follower.create(user=self.user, username=username)
            self.followers.append(f)

    def test_controller_create_user(self):
        c = Controller(username='pepe')
        self.assertEqual(c.user.username, 'pepe')
        self.assertTrue(c.is_new)

    def test_controller_exists_user(self):
        c = Controller(username='darude')
        self.assertEqual(c.user.username, 'darude')
        self.assertFalse(c.is_new)

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

    def test_get_users_to_unfollow(self):
        c = Controller(username='pepe')
        users = c.get_users_to_unfollow()
        print(users)
        self.assertTrue(len(users))


if __name__ == '__main__':
    unittest.main()
