import os
from pyinstamation import config
import json

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


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


def format_post(post):
    node = post.get('node', {})
    code = node.get('shortcode')
    captions = node.get('edge_media_to_caption', {}).get('edges', [])
    c = captions[0]
    caption = c.get('node', {}).get('text')
    return {
        'code': code,
        'caption': caption,
    }


def posts_parser(json_content):
    hashtag = json_content.get('graphql', {}).get('hashtag', {})
    posts = hashtag.get('edge_hashtag_to_top_posts', {}).get('edges', [])
    posts += hashtag.get('edge_hashtag_to_media', {}).get('edges', [])
    if len(posts) == 0:
        return []
    return map(format_post, posts)
