
import os
import time

from unittest import TestCase
from unittest.mock import patch, MagicMock

from codequick import Listitem

from resources.lib.channels.uk import my5

from testutils import open_doc, HttpResponse


my_dir = os.path.abspath(os.path.dirname(__file__))


class TestMainPage(TestCase):
    @patch('urlquick.get',
           side_effect=(
                   HttpResponse(200, text=open_doc('PLC_My5DesktopHeroRail.json', my_dir)),
                   HttpResponse(200, text=open_doc('hero_content.json', my_dir)))
           )
    def test_parse_hero_items(self, _):
        li_items = my5.list_collections.test('hero')
        self.assertEqual(11, len(li_items))
        for li in li_items:
            self.assertIsInstance(li, Listitem)

    @patch('urlquick.get',
           side_effect=(
                   HttpResponse(200, text=open_doc('PLC_My5DesktopHeroRail.json', my_dir)),
                   HttpResponse(200, text=open_doc('hero_content.json', my_dir)))
           )
    def test_list_main_page(self, _):
        li_items = my5.list_main_page.test()
        self.assertEqual(14, len(li_items))
        for li in li_items:
            self.assertIsInstance(li, Listitem)

@patch('resources.lib.channels.uk.my5.get_session_token', return_value='kjg')
class TestMy5(TestCase):
    @patch('urlquick.get',
           return_value=HttpResponse(200, text=open_doc('chan5_continuewatching.json', my_dir)))
    def test_continue_watching(self, _, __):
        li_items = my5.list_continue_watching.test()
        self.assertEqual(13, len(li_items))
        for li in li_items:
            self.assertIsInstance(li, Listitem)


class TestUtils(TestCase):
    @patch('urlquick.get',
           return_value=HttpResponse(200, text=open_doc('chan5_watchables_search.json', my_dir)))
    def test_search_watchable(self, _):
        li_items = list(my5.search_watchables(MagicMock(), ['1', '2', '3', '4']))
        self.assertEqual(19, len(li_items))
        for li in li_items:
            self.assertIsInstance(li, Listitem)

    def test_availability(self):
        now = time.time() + 1
        result = my5.availability(now + 366 * 86400)
        self.assertEqual(result, 'Available for over a year.')
        result = my5.availability(now + 365 * 86400)
        self.assertEqual(result, 'Available for 12 months.')
        result = my5.availability(now + 65 * 86400)
        self.assertEqual(result, 'Available for 2 months.')
        result = my5.availability(now + 32 * 86400)
        self.assertEqual(result, 'Available for 1 month.')
        result = my5.availability(now + 30 * 86400)
        self.assertEqual(result, '[COLOR orange]Only 30 days available.[/COLOR]')
        result = my5.availability(now + 24 * 3600)
        self.assertEqual(result, '[COLOR orange]Only 1 day available.[/COLOR]')
        result = my5.availability(now + 23 * 3600)
        self.assertEqual(result, '[COLOR orange]Only 23 hours available.[/COLOR]')
        result = my5.availability(now + 3600)
        self.assertEqual(result, '[COLOR orange]Only 1 hour available.[/COLOR]')
        result = my5.availability(now + 1800)
        self.assertEqual(result, '[COLOR orange]Only 0 hours available.[/COLOR]')