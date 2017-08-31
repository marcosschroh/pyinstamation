import os
from urllib.parse import urlparse
from pyinstamation.config import SAVE_SOURCE


TEST_LOCATION = 'tests/static'


def save_page_source(url, source, location=None):
    if not SAVE_SOURCE:
        return

    if location is None:
        location = TEST_LOCATION
    o = urlparse(url)
    filename = o.path.strip('/').replace('/', '.') + '.html'
    filepath = os.path.join(location, filename)
    with open(filepath, 'w') as f:
        f.write(source)
