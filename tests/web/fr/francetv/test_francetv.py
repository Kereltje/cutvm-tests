import requests

from unittest import TestCase

from resources.lib.channels.fr import francetv

from credentials import credentials


class TestListLiveWithEPG(TestCase):
    def test_france_live(self):
        li = francetv.get_live_url.test('france-2')
        pass