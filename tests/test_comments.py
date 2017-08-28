import random
import unittest
from pyinstamation import comments


class CommentTestCase(unittest.TestCase):

    def setUp(self):
        random.seed(1234)

    def test_symbol_generator_fixed_symbol(self):
        SYMBL = '!'
        symbol = comments.symbol_generator(symbol=SYMBL)
        self.assertIn(SYMBL, symbol)

    def test_symbol_generator_rand(self):
        symbol = comments.symbol_generator()
        self.assertEqual(symbol, ':)')

    def test_letter_repetition_prob_null(self):
        WORD = 'awesome'
        word = comments.letter_repetition(WORD, probability=0)
        self.assertEqual(word, WORD)

    def test_letter_repetition_prob_max(self):
        WORD = 'awesome'
        word = comments.letter_repetition(WORD, probability=1)
        self.assertEqual(word, 'awesssome')

    def test_comment_no_type(self):
        comment = comments.comment()
        self.assertEqual(comment, 'this shot is awesome')

    def test_comment_type_photo(self):
        comment = comments.comment(post_type='photo')
        self.assertEqual(comment, 'this photo is awesome')

    def test_comment_type_video(self):
        comment = comments.comment(post_type='video')
        self.assertEqual(comment, 'this vid is awesome')
