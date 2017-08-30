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
    USERS_PATTERN = re.compile(r'/users')

    def do_GET(self):
        # if re.search(self.USERS_PATTERN, self.path):
        self.send_response(200)

        # Add response headers.
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        self.wfile.write(b'<html><body><p>OK</p></body></html>')
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
