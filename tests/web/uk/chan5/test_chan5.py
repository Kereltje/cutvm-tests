from unittest import TestCase
from unittest.mock import patch

import urlquick
from codequick import Listitem

from credentials import credentials
from resources.lib.channels.uk import my5


UNAME = credentials['uk']['chan5']['uname']
PASSW = credentials['uk']['chan5']['passw']
TOKEN = credentials['uk']['chan5']['auth_token']


class Login(TestCase):
    def test_perform_sign_in_request(self):
        result = my5.perform_signin_request(UNAME, PASSW)
        self.assertIs(result, True)

    def test_perform_sign_in_request_with_invalid_passw(self):
        with self.assertRaises(urlquick.HTTPError) as err_result:
            my5.perform_signin_request(UNAME, 'adsa')
        err = err_result.exception
        self.assertEqual(str(err), 'Incorrect username or password.')


class TestMenu(TestCase):
    def test_main_page(self):
        items = list(my5.list_main_page.test())
        self.assertAlmostEqual(len(items), 15, delta=2)
        for item in items:
            self.assertIsInstance(item, Listitem)

    def test_submenu_my5(self):
        items = list(my5.list_submenu_my5.test())
        self.assertEqual(len(items), 3)
        for item in items:
            self.assertIsInstance(item, Listitem)


@patch('resources.lib.channels.uk.my5.get_session_token', return_value=TOKEN)
class TestMy5Submenu(TestCase):
    def test_mylist(self, _):
        """Assume some items are on the list."""
        items = list(my5.list_my_list_shows.test())
        for item in items:
            self.assertIsInstance(item, Listitem)

    def test_recommendations(self,_):
        items = list(my5.list_recommendations.test())
        self.assertEqual(10, len(items))
        for item in items:
            self.assertIsInstance(item, Listitem)

    def test_continue_watching(self,_):
        items = list(my5.list_continue_watching.test())
        self.assertEqual(15, len(items))
        for item in items:
            self.assertIsInstance(item, Listitem)