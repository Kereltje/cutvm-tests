import os
import json
from unittest import TestCase
from unittest.mock import patch

from codequick import Listitem

from credentials import credentials
from resources.lib.channels.uk import channel4

import xbmcaddon

UNAME = credentials['uk']['chan4']['uname']
PASSW = credentials['uk']['chan4']['passw']
TOKENS = {}


def read_tokens():
    global TOKENS
    cache_file = os.path.join(os.environ['KODI_PROFILE'], 'addon_data/plugin.video.catchuptvandmore/channel4_auth.json')
    with open(cache_file, 'r') as f:
        TOKENS = json.load(f)


def setUpModule():
    channel4.CACHE_FILE = os.path.abspath(
        channel4.CACHE_FILE.replace('special://userdata', os.environ['KODI_PROFILE']))
    read_tokens()


class TestSearch(TestCase):
    def test_search_with_results(self):
        items = list(channel4.do_search.test("murder"))
        self.assertGreater(len(items), 4)
        for item in items:
            self.assertIsInstance(item, Listitem)

    @patch('xbmcgui.Dialog.ok')
    def test_search_without_results(self, _):
        items = list(channel4.do_search.test("poeliejoepa"))
        self.assertEqual(len(items), 1)
        self.assertIs(items[0], False)


class TestLogin(TestCase):
    def test_login(self):
        result = channel4.login(UNAME, PASSW)
        self.assertIsNotNone(result)
        return result

    def test_refresh(self):
        result = channel4.refresh(TOKENS['refreshToken'])
        self.assertIsNotNone(result)
        TOKENS['accessToken'] = result
        return result
