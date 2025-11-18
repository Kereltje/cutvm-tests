from unittest import TestCase

import urlquick

from credentials import credentials
from resources.lib.channels.uk import my5


UNAME = credentials['uk']['chan5']['uname']
PASSW = credentials['uk']['chan5']['passw']


class Login(TestCase):
    def test_perform_sign_in_request(self):
        result = my5.perform_signin_request(UNAME, PASSW)
        self.assertIs(result, True)

    def test_perform_sign_in_request_with_invalid_passw(self):
        with self.assertRaises(urlquick.HTTPError) as err_result:
            my5.perform_signin_request(UNAME, 'adsa')
        err = err_result.exception
        self.assertEqual(str(err), 'Incorrect username or password.')

