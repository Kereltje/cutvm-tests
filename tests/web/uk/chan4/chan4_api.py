
import requests

from unittest import TestCase


from credentials import credentials


UNAME = credentials['uk']['chan4']['uname']
PASSW = credentials['uk']['chan4']['passw']
CAPTCHA_TKN = credentials['uk']['chan4']['captchaToken']

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'


class TestLogin(TestCase):
    def test_login_web(self):
        with requests.Session() as sess:
            sess.headers = {
                'user-agent': USER_AGENT,
                'accept-language': 'en-GB,en;q=0.5',
                'origin': 'https://www.channel4.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
            }
            # Pick up some cookies
            resp = sess.get(
                url='https://www.channel4.com/sign-in-or-register',
                headers={
                    'referer': 'https://www.channel4.com/',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-dest': 'document',
                },
                params={
                    'redirectUrl': 'https://www.channel4.com/',
                    'intcmp': 'platform:header:sign_in::|::||',
                    'source':  'global_nav'
                }
            )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(resp.history), 1)

            resp = sess.post(
                url='https://www.channel4.com/identity/sign-in',
                headers={
                    'user-agent': USER_AGENT,
                    'content-type': 'application/json',
                    'accept-language': 'en-GB,en;q=0.5',
                    'referer': 'https://www.channel4.com/sign-in?redirectUrl=https%3A%2F%2Fwww.channel4.com%2F'
                },
                json={
                    'captchaToken': CAPTCHA_TKN,
                    'email': UNAME,
                    'password': PASSW
                }
            )
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertEqual(data['message'], 'Successfully signed in')
            cookies = resp.cookies
            self.assertTrue('4id_Identity' in cookies)
            self.assertTrue('4id_Session' in cookies)

    def test_login_firestick(self):
        """Mimic login from a firestick TV

        URL and user-agent string from https://github.com/Catch-up-TV-and-More/plugin.video.catchuptvandmore/issues/1606
        """
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 11; AFTKM Build/RS8116.2387N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.248 Mobile Safari/537.36 All4/7.4.0-release',
            # 'authorization': 'Basic eUExTHB6dGtHZUhaRDZuU2E3QzFBQUY2dkhwelZOblU6UXFFbUVnVVVVT1hUa3piNg=='
        }
        # Get auth token
        resp = requests.get(
            url='https://api.channel4.com/online/v2/auth/pin',
            headers = headers)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.headers['authorization'], headers['authorization'])
        pin_data  = resp.json()

        # # Verify Email
        # headers['authorization'] = 'Bearer jfeoBPdSObNHLu4mByJUeLJ4QZMy'
        # resp = requests.post(
        #     url='https://api.channel4.com/online/v1/identity/user/email',
        #     headers=headers,
        #     json={'emailAddress': UNAME}
        # )
        # self.assertEqual(200, resp.status_code)
        # self.assertDictEqual(resp.json(), {"available": False})

        # login
        headers['authorization'] = 'Basic eUExTHB6dGtHZUhaRDZuU2E3QzFBQUY2dkhwelZOblU6UXFFbUVnVVVVT1hUa3piNg=='
        resp = requests.post(
            url='https://api.channel4.com/online/v2/auth/token?client=amazonfire-dash',
            headers=headers,
            data={'username': UNAME, 'password': PASSW, 'grant_type': 'password'}
        )
        self.assertEqual(200, resp.status_code)
        rsp_data = resp.json()
        pass


class TestCategories(TestCase):
    def test_category_default_page_size(self):
        resp = requests.get('https://www.channel4.com/categories/drama?sort=az&json=true')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreater(data['noOfShow'], 300)
        self.assertTrue('pageTitle' in data)
        self.assertTrue('baseUrl' in data)
        self.assertFalse(data['user']['authenticated'])
        items = data['brands']['items']
        self.assertEqual(60, len(items))

    def test_category_page_size(self):
        """Test the effect of parameter `size`

        Does not seem to have any effect.
        """
        resp = requests.get('https://www.channel4.com/categories/drama?sort=az&json=true&limit=400')
        data = resp.json()
        self.assertEqual(60, len(data['brands']['items']))
        resp = requests.get('https://www.channel4.com/categories/drama?sort=az&json=true&offset=120&limit=20')
        data = resp.json()
        self.assertEqual(60, len(data['brands']['items']))