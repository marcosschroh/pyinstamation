import unittest
from pyinstamation import config


class UtilsTestCase(unittest.TestCase):

    def test_load_config(self):
        config.load_config(filepath='test.config.yaml')
        self.assertEqual(config.CONFIG['username'], 'discovrar')
        self.assertEqual(config.CONFIG['password'], 'discorvd')
        self.assertEqual(config.CONFIG['testing'], True)

    def test_load_config_twice(self):
        config.load_config(filepath='test.config.yaml')
        result = config.load_config()
        self.assertIsNone(result)

    def test_load_config_syntax_error_yaml(self):
        with self.assertRaises(SystemExit):
            config.load_config(filepath='tests/static/syntax.error.config.yaml')
