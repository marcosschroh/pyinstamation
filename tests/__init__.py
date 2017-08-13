import unittest
import peewee
from playhouse.test_utils import test_database
from pyinstamation import models


class DBTestCase(unittest.TestCase):
    TEST_DB = peewee.SqliteDatabase(':memory:')

    def run(self, result=None):
        with test_database(self.TEST_DB, (models.User, models.Follower)):
            super().run(result)
