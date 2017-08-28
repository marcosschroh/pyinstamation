import random


PRONOUN = ["this"]
POST_TYPES = {
    'photo': ['photo', 'pic', 'picture', 'snapshot'],
    'video': ['vid', 'video'],
    'other': ['shot', 'post', 'view']
}
CONNECTORS = ["is", "looks", "feels", "is really", 'is truly', 'is so']
ADJECTIVES = [
    'adorable', 'amazing', 'awesome', 'beautiful', 'cool', 'delightful', 'epic',
    'excellent', 'fabulous', 'fantastic', 'glorious', 'good', 'gorgeous', 'great',
    'incredible', 'lovely', 'magical', 'magnificent', 'nice', 'prodigious',
    'stunning', 'unbelievable', 'wonderful',
]

EXPRESSIONS = [
    'blew my mind',
    'wow'
]

PHRASE_OPTIONS = [
    '{pronoun} {post_type} {connector} {adjective}{symbol}',
    '{pronoun} {post_type} {expression}{symbol}',
    '{adjective} {post_type}{symbol}',
    '{adjective}{symbol}',
    '{pronoun} {expression}{symbol}'
]


def symbol_generator(symbol=None):
    """Appends to the end of a word.

    :returns: ' !' or '!!' or ':D', note that some have an space
    :rtype: str
    """
    if symbol is None:
        symbols = ['', '.', '!', ':)', ':D']
        symbol = random.choice(symbols)
    return (' ' * random.choice([0, 1])) + (symbol * random.randrange(1, 4))


def letter_repetition(word, probability=0.2):
    """ Repeats a random letter of word

    :type word: str
    :probability: between 0 and 1
    :type probability: float
    :rtype: str
    """
    if random.random() > probability:
        return word
    letter_pos = random.choice(range(len(word)))
    times_to_repeat = random.randrange(2, 6)
    letter_to_repeat = word[letter_pos]

    _word = list(word)
    repeated_word = _word[:letter_pos] + [letter_to_repeat] * times_to_repeat + _word[letter_pos:]
    return ''.join(repeated_word)


def comment(post_type=None):
    """Generates a trivial random comment.

    :type post_type: str or None
    :rtype: str
    """
    if post_type is not None:
        _posts_type = POST_TYPES[post_type] + POST_TYPES['other']
    else:
        _posts_type = POST_TYPES['other']

    _components = {
        'pronoun': random.choice(PRONOUN),
        'post_type': random.choice(_posts_type),
        'connector': random.choice(CONNECTORS),
        'adjective': letter_repetition(random.choice(ADJECTIVES)),
        'expression': random.choice(EXPRESSIONS),
        'adj_or_expr': letter_repetition(random.choice(ADJECTIVES + EXPRESSIONS)),
        'symbol': symbol_generator()
    }
    return random.choice(PHRASE_OPTIONS).format(**_components).strip()
