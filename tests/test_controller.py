import unittest
import datetime
from collections import namedtuple
from pyinstamation.models import User, Follower
from pyinstamation.controller import Controller
from tests import DBTestCase


class ModelTest(DBTestCase):

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

    def test_get_users_following_list(self):
        c = Controller
        self.assertFalse(False)


if __name__ == '__main__':
    unittest.main()
