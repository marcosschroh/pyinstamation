import os
from urllib.parse import quote
from pyinstamation import config
import json


TEST_LOCATION = 'tests/static'


def save_page_source(path, source, location=None):

    if not config.SAVE_SOURCE:
        return None

    if location is None:
        location = TEST_LOCATION

    if not isinstance(source, str):
        source = json.dumps(source)

    filename = quote(path.strip('/') or '/', safe='') + '.html'
    filepath = os.path.join(location, filename)

    with open(filepath, 'w') as f:
        f.write(source)

    return filepath
