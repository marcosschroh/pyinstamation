import os
import unittest

from pyinstamation.scrapper import utils
from pyinstamation import config


URL = 'https://www.instagram.com/random/url/users'
CONTENT = '''
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>302 Moved</TITLE></HEAD><BODY>
<H1>302 Moved</H1>
The document has moved
<A HREF="https://www.google.nl/?gfe_rd=cr&amp;dcr=0&amp;ei=KzesWZWQNPHG8AeTk5a4DA">here</A>.
</BODY></HTML>
'''


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.filepath = None

    def tearDown(self):
        if self.filepath:
            os.remove(self.filepath)

    def test_save_page_source_allowed(self):
        config.SAVE_SOURCE = True
        self.filepath = utils.save_page_source(URL, CONTENT)
        self.assertTrue(os.path.exists(self.filepath))

    def test_save_page_source_not_allowed(self):
        config.SAVE_SOURCE = False
        self.filepath = utils.save_page_source(URL, CONTENT)
        self.assertIsNone(self.filepath)
