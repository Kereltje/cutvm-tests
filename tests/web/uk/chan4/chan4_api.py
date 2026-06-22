import time
import os
import json

import re
import requests

from unittest import TestCase
from datetime import datetime, timedelta, timezone

import xbmcaddon

from credentials import credentials
from web.uk.chan4 import test_chan4
from resources.lib.channels.uk import channel4

UNAME = credentials['uk']['chan4']['uname']
PASSW = credentials['uk']['chan4']['passw']
# CAPTCHA_TKN = credentials['uk']['chan4']['captchaToken']
TOKENS = {}
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'


def read_tokens():
    global TOKENS
    cache_file = os.path.join(os.environ['KODI_PROFILE'], 'addon_data/plugin.video.catchuptvandmore/channel4_auth.json')
    with open(cache_file, 'r') as f:
        TOKENS = json.load(f)


def setUpModule():
    xbmcaddon.Addon._Addon__settings['plugin.video.catchuptvandmore']['uk.channel4.login'] = UNAME
    xbmcaddon.Addon._Addon__settings['plugin.video.catchuptvandmore']['uk.channel4.password'] = PASSW
    channel4.CACHE_FILE = os.path.abspath(
        channel4.CACHE_FILE.replace('special://userdata', os.environ['KODI_PROFILE']))
    read_tokens()
    if int(TOKENS['issuedAt']) / 1000 + int(TOKENS['expiresIn']) < time.time() + 300:
        test_case = test_chan4.TestLogin()
        test_case.test_refresh()
        read_tokens()


class TestLogin(TestCase):
    def test_recaptcha(self):
        resp = requests.get(
            url='https://www.channel4.com/sign-in-or-register',
            headers={
                'user-agent': USER_AGENT,
                'accept-language': 'en-GB,en;q=0.5',
                'origin': 'https://www.channel4.com',
                'sec-fetch-site': 'same-origin',
                'referer': 'https://www.channel4.com/',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-dest': 'document',
            }
        )
        site_key = re.search(r'"siteKey":"(\w+)",', resp.text)

        resp = requests.post(
            url='https://www.google.com/recaptcha/enterprise/reload?k=' + site_key,
            headers={
                'user-agent': USER_AGENT,
                'accept-language': 'en-GB,en;q=0.5',
                'origin': 'https://www.google.com',
                'referer': 'https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Leyk3gbAAAAAFXvdqcW04M6tVBCBxkn2u4176Js&co=aHR0cHM6Ly93d3cuY2hhbm5lbDQuY29tOjQ0Mw..&hl=en&v=U5VsmTDhJM1iOJUyw4DEUTYv&size=invisible&anchor-ms=20000&execute-ms=30000&cb=d4cgz5olg2uz_GRECAPTCHA=09AKhCRwhzPEpWhAzqfSakVksWIkDcb-ND38_qIW6K5dqasoQSCJmJdzNuZ-mlo399pEOv4u5vmcBUZAN91S7NI7I',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
            }

        )


    def test_login(self):
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


class TvPairing(TestCase):
    HEADERS = {
        'user_agent': 'Mozilla/5.0 (Linux ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Safari/537.36 OPR/46.0.2207.0 OMI/4.23.2.96.LIMA2.85 Model/Vestel-MB181 VSTVB MB100 FVC/8.0 (BUSH; MB181; ) HbbTV/1.6.1 (+DRM; BUSH; MB181; 3.9.5.0; ; _TV_G36_2023;) SmartTv',
        'authorization': 'Basic Z0FJY0hFRjZZOUJ2akVMNnR4azF2TDZyQ1htQW5hZnA6MjRIYnRqSkp2SDNjTHQ4MA==',
        'origin': 'https://google.bsd.client.streaming.channel4.com',
        'Referer': 'https://google.bsd.client.streaming.channel4.com/'
    }

    def get_pin(self):
        resp = requests.get(
            'https://api.channel4.com/online/v2/auth/pin',
            headers=self.HEADERS
        )
        self.assertEqual(resp.status_code, 200)
        resp_data = resp.json()
        self.assertTrue('userCode' in resp_data)
        self.assertTrue('deviceCode' in resp_data)
        self.assertEqual(resp_data['expiresIn'], 600)
        self.assertEqual(resp_data['nextPollIn'], 5)
        self.assertEqual(resp_data['verification']['url'], 'channel4.com/code')
        create_date = datetime.fromisoformat(resp_data['createDate'])
        self.assertAlmostEqual(create_date, datetime.now(tz=timezone.utc), delta=timedelta(seconds=2))
        self.assertTrue('urlForStaticQr' in resp_data['verification'])
        self.assertTrue('urlForDynamicQr' in resp_data['verification'])
        return resp_data

    def check_token(self, device_code, create_date, expected_result=False):
        """Check whether login and paring with another device has succeeded.
        """
        resp = requests.post(
            'https://api.channel4.com/online/v2/auth/token',
            json={
                'grant_type': 'pin_pairing',
                'code': device_code,
                'create_date': create_date
            }
        )
        self.assertEqual(resp.status_code, 200)
        resp_data = resp.json()
        self.assertIs(resp_data['paired'], expected_result)
        if expected_result is False:
            self.assertEqual(len(resp_data), 1)
        else:
            for field in ('accessToken', 'refreshToken', 'c4id', 'securityToken'):
                self.assertTrue(resp_data[field])
            self.assertEqual(resp_data['tokenType'], 'BearerToken')
            self.assertAlmostEqual(int(resp_data['expiresIn']), 10799, delta=500)                   # 3 hours
            self.assertAlmostEqual(int(resp_data['issuedAt']), time.time(), delta=10)
            self.assertAlmostEqual(int(resp_data['refreshTokenExpiresIn']), 63071999, delta=500)    # 2 years
            self.assertAlmostEqual(int(resp_data['refreshTokenIssuedAt']), time.time(), delta=10)


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