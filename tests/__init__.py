import os
import logging
import unittest
import peewee
from playhouse.test_utils import test_database
from pyinstamation import models
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import socket
from threading import Thread


logging.disable(logging.CRITICAL)


class DBTestCase(unittest.TestCase):
    TEST_DB = peewee.SqliteDatabase(':memory:')

    def run(self, result=None):
        with test_database(self.TEST_DB, (models.User, models.Follower)):
            super().run(result)


class MockServerRequestHandler(BaseHTTPRequestHandler):

    URL_ACC = re.compile(r'accounts.login.html')
    URL_TAG = re.compile(r'explore.tags.(?P<tag>[\w-]+)')
    URL_POST = re.compile(r'p.(?P<post_id>[\w-]+)')
    URL_USER = re.compile(r'(?P<username>[\w-]+)')

    URL_LOGIN_REDIRECT = r'accounts/login?username=discovrar&password=discorvd'

    def format_path(self, path):
        return path.replace('/', '.').strip('.')

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')

        if re.search(self.URL_LOGIN_REDIRECT, self.path):
            self.send_header('Set-Cookie', 'sessionid=c295IGVsIHVzdWFyaW8gZnVsYW5pdG8K')

        self.end_headers()
        # if re.search(self.URL_ACC, path) or re.search(self.URL_TAG, path):
        #     pass
        # elif re.search(self.URL_POST, path):
        #     pass
        # elif re.search(self.URL_USER, path):
        #     pass
        # Add response headers.

        filename = self.format_path(self.path)
        filepath = os.path.join('./tests/static', '{0}.html'.format(filename))

        try:
            f = open(filepath, 'rb')
        except FileNotFoundError:
            self.send_response(404)
            self.wfile.write(b'\n<html><body>404 Not Found!</body></html>')
        else:
            self.send_response(200)
            # needs an extra new line
            self.wfile.write(b'\n' + f.read())

            f.close()
        return

    def log_message(self, format, *args):
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
