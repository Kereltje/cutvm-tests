import os
import json
from unittest import TestCase
from unittest.mock import patch

from codequick import Listitem

from credentials import credentials
from resources.lib.channels.uk import channel4


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


class MainMenu(TestCase):
    def test_main_menu(self):
        items = channel4.main_menu.test()
        self.assertGreater(len(items), 10)


class TestCategoryContent(TestCase):
    def test_category_drama(self):
        items = channel4.list_programs.test('https://www.channel4.com/categories/drama?sort=az&json=true', 0)
        self.assertGreater(len(items), 10)


class TestListSeasons(TestCase):
    def test_list_season_with_single_item(self):
        # A Brand with a single item , i'e' a film
        url = ('https://www.channel4.com/programmes/11-men-against-11?'
               'intcmp=categories%3Aslice%3A%3Ap1%3Al1%7CDISCOVERY%3Adrama.none.none.az%7C%7C')
        list_items = channel4.list_seasons.test(url)
        self.assertEqual(len(list_items), 1)

    def test_list_episode_programme_with_one_season(self):
        # Bergerac
        url = ('https://www.channel4.com/programmes/bergerac?'
               'intcmp=categories%3Aslice%3A%3Ap1%3Al42%7CDISCOVERY%3Adrama.none.none.az%7C%7C')
        list_items = channel4.list_seasons.test(url)
        self.assertGreater(len(list_items), 3)

    def test_list_seasons_of_programme_with_multiple_seasons(self):
        # The Bold Type
        url = ('https://www.channel4.com/programmes/the-bold-type?'
               'intcmp=categories%3Aslice%3A%3Ap1%3Al58%7CDISCOVERY%3Adrama.none.none.az%7C%7C')
        list_items = channel4.list_seasons.test(url)
        self.assertGreater(len(list_items), 5)


class UserList(TestCase):
    def test_mylist_items(self):
        channel4.my_list_programmes = None
        mylist = channel4.get_mylist_programmes()
        self.assertGreater(len(mylist), 1)

    def test_list_my_list(self):
        items = channel4.list_my_four.test('MYLIST')
        self.assertGreater(len(items), 5)

    def test_list_history(self):
        items = channel4.list_my_four.test('HISTORY')
        self.assertGreater(len(items), 5)

    def test_list_recommendations(self):
        items = channel4.list_my_four.test('RECOMMENDATIONS')
        self.assertGreater(len(items), 5)

    def test_list_watching(self):
        items = channel4.list_my_four.test('CONTINUE_WATCHING')
        self.assertGreater(len(items), 1)


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
