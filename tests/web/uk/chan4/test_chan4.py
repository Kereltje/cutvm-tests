from unittest import TestCase
from unittest.mock import patch

import urlquick
from codequick import Listitem

from credentials import credentials
from resources.lib.channels.uk import channel4

import xbmcaddon


UNAME = credentials['uk']['chan4']['uname']
PASSW = credentials['uk']['chan4']['passw']


def setUpModule():
    xbmcaddon.Addon._Addon__settings['plugin.video.catchuptvandmore']['uk.channel4.login'] = UNAME
    xbmcaddon.Addon._Addon__settings['plugin.video.catchuptvandmore']['uk.channel4.password'] = PASSW


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