import os
from urllib.parse import quote
from pyinstamation import config


TEST_LOCATION = 'tests/static'


def save_page_source(path, source, location=None):

    if not config.SAVE_SOURCE:
        return None

    if location is None:
        location = TEST_LOCATION

    filename = quote(path.strip('/'), safe='') + '.html'
    filepath = os.path.join(location, filename)

    with open(filepath, 'w') as f:
        f.write(source)

    return filepath
