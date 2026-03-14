
import os
import time

from unittest import TestCase
from unittest.mock import patch, MagicMock

import urlquick
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


class TestIvDataRetry(TestCase):
    """Since it's unknown in which order hmac and aes keys appear in the set of keys passed
    to iv_data(), the function just tries one and if the server return 403, swaps the keys
    and retries.

    """
    def setUp(self):
        self.keys =  ('bcdefghijklmnopqrstuvw==', 'BCDAFGHIJKLMNOPGRSTUVW==')

    @patch('urlquick.get', return_value=HttpResponse(text=open_doc('data/stream_data.json', my_dir)))
    def test_iv_data_without_swap(self, p_get):
        iv, data, aeskey = my5.ivdata('ITEMID', 'media', self.keys)
        self.assertEqual(aeskey, self.keys[0])
        p_get.assert_called_once()

    @patch('codequick.script.Settings.__setitem__')
    @patch('urlquick.get', return_value=HttpResponse(text=open_doc('data/stream_data.json', my_dir)))
    @patch('resources.lib.channels.uk.my5.Script.setting.get_boolean',
           new=lambda x: True if x == my5.SETTING_ID_KEYS_REVERSED else False)
    def test_iv_data_swapped_by_setting(self, p_get, p_settings_set):
        iv, data, aeskey = my5.ivdata('ITEMID', 'media', self.keys)
        self.assertEqual(aeskey, self.keys[1])
        p_get.assert_called_once()
        p_settings_set.assert_not_called()

    @patch('codequick.script.Settings.__setitem__')
    @patch('urlquick.get', side_effect=(
            urlquick.HTTPError(response=HttpResponse(403)),
            HttpResponse(text=open_doc('data/stream_data.json', my_dir))))
    def test_iv_data_swapped_by_403_response(self, p_get, p_settings_set):
        iv, data, aeskey = my5.ivdata('ITEMID', 'media', self.keys)
        self.assertEqual(aeskey, self.keys[1])
        self.assertEqual(2, p_get.call_count)
        p_settings_set.assert_called_once_with(my5.SETTING_ID_KEYS_REVERSED, 'true')

    @patch('urlquick.get', side_effect=urlquick.HTTPError(response=HttpResponse(403)))
    def test_iv_data_fails_on_second_attempt(self, p_get):
        """Should fail after retry"""
        self.assertRaises(urlquick.HTTPError, my5.ivdata, 'ITEMID', 'media', self.keys)
        self.assertEqual(2, p_get.call_count)

    @patch('urlquick.get', side_effect=urlquick.HTTPError(response=HttpResponse(400)))
    def test_iv_data_fails_on_other_http_error(self, p_get):
        """Should fail immediately, without retry"""
        self.assertRaises(urlquick.HTTPError, my5.ivdata, 'ITEMID', 'media', self.keys)
        p_get.assert_called_once()

    @patch('urlquick.get', side_effect=urlquick.ConnectTimeout)
    def test_iv_data_fails_on_other_error(self, p_get):
        """Should fail immediately, without retry"""
        self.assertRaises(urlquick.ConnectTimeout, my5.ivdata, 'ITEMID', 'media', self.keys)
        p_get.assert_called_once()