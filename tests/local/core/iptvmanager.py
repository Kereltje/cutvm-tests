
from socketserver import TCPServer, BaseRequestHandler

from unittest import TestCase
from unittest.mock import patch, MagicMock

from resources.lib import iptvmanager


@patch("resources.lib.iptvmanager.IPTVManager.via_socket", lambda x: x)
class TestIptvEpg(TestCase):
    def setUp(self):
        self.port = 43516
        self.servr = TCPServer(('0.0.0.0', self.port), BaseRequestHandler)

    def tearDown(self):
        self.servr.server_close()

    def test_send_epg(self):
        iptvmanager.epg.test(self.port)


