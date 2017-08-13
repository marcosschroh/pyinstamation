import unittest
import peewee

from pyinstamation import models
from tests import DBTestCase


class ControllerTest(DBTestCase):

    def test_holis(self):
        self.assertTrue('willy')


if __name__ == '__main__':
    unittest.main()
