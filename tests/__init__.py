import os
import re
import peewee
import socket
import unittest
import logging
from threading import Thread
from urllib.parse import quote
from pyinstamation import models
from playhouse.test_utils import test_database
from http.server import BaseHTTPRequestHandler, HTTPServer


MOCK_HOSTNAME = 'http://localhost:{port}/'
logging.disable(logging.CRITICAL)


class DBTestCase(unittest.TestCase):
    TEST_DB = peewee.SqliteDatabase(':memory:')

    def run(self, result=None):
        with test_database(self.TEST_DB, (models.User, models.Follower)):
            super().run(result)


class MockServerRequestHandler(BaseHTTPRequestHandler):

    LOGGED = re.compile(r'username=(?P<username>[\w-]+)&password=(?P<password>[\w-]+)')

    def format_path(self, path):
        return path.replace('/', '.').strip('.')

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Set-Cookie', 'sessionid=c295IGVsIHVzdWFyaW8gZW5pdG8K')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @property
    def filepath(self):
        if len(self.path) < 2 or self.logged:
            filename = '%2F'
        else:
            filename = quote(self.path.strip('/'), safe='')
        return os.path.join('./tests/static', '{0}.html'.format(filename))

    def _read_from_file_or_404(self):
        try:
            f = open(self.filepath, 'rb')
        except FileNotFoundError:
            self.send_response(404)
            self.wfile.write(b'\n<html><body>404 Not Found!</body></html>')
        else:
            self.send_response(200)
            # needs an extra new line
            self.wfile.write(b'\n' + f.read())

            f.close()

    def _match_url(self):
        self.logged = bool(self.LOGGED.search(self.path))

    def do_GET(self):
        self._match_url()
        self._set_headers()
        self._read_from_file_or_404()

    def do_POST(self):
        self._set_headers()
        self._read_from_file_or_404()

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
    return mock_server_thread
