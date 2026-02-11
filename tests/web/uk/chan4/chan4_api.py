"""
WARNING:
    Using these tests one can easily hit an HTTP 429 error : "Login attempt amount exceeded".
    In order to separate the result of one test from another, some tests concerning login,
    refresh and logout do their own login. The number of allowed attempts is unknown to me,
    but running all these tests in quick succession will most likely cause problems.
"""

from __future__ import annotations
import time
import os
import json
from uuid import uuid4

import re
import requests

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from unittest import TestCase
from datetime import datetime, timedelta, timezone

import xbmcaddon

from credentials import credentials

from web.uk.chan4.device_data import devices, allowed_clients


UNAME = credentials['uk']['chan4']['uname']
PASSW = credentials['uk']['chan4']['passw']
# DEVICE = 'freeview-hp'
DEVICE = 'amazon-fos8'
# CAPTCHA_TKN = credentials['uk']['chan4']['captchaToken']
TOKENS = {}
AUTH_CACHE_PATH = os.path.join(str(os.path.dirname(__file__)),  'channel4_auth.json')
WEB_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'


def read_tokens():
    global TOKENS

    try:
        with open(AUTH_CACHE_PATH, 'r') as f:
            TOKENS = json.load(f)
    except FileNotFoundError:
        TOKENS = {}


def save_tokens():
    with open(AUTH_CACHE_PATH, 'w') as f:
        json.dump(TOKENS, f)


def ensure_signed_in(device: str = DEVICE):
    if not TOKENS:
        read_tokens()

    device_tokens = TOKENS.get(device)
    if device_tokens:
        if int(device_tokens['issuedAt']) / 1000 + int(device_tokens['expiresIn']) > time.time() + 300:
            return
        else:
            resp = APiRefreshTokens.refresh(device, device_tokens['refreshToken'])
            if resp.status_code == 200:
                TOKENS[device] = resp.json()
                save_tokens()
                return
    resp = api_login(UNAME, PASSW, device)
    resp.raise_for_status()
    TOKENS[device] = resp.json()
    save_tokens()


def check_auth_data(testcase: TestCase, resp_data: dict):
    for field in ('accessToken', 'refreshToken', 'c4id', 'securityToken'):
        testcase.assertTrue(resp_data[field])
    testcase.assertEqual(resp_data['tokenType'], 'BearerToken')
    testcase.assertIsInstance(resp_data['expiresIn'], str)
    testcase.assertAlmostEqual(int(resp_data['expiresIn']), 10799, delta=500)  # 3 hours
    testcase.assertIsInstance(resp_data['issuedAt'], str)
    testcase.assertAlmostEqual(int(resp_data['issuedAt'])/1000, time.time(), delta=10)
    testcase.assertIsInstance(resp_data['refreshTokenExpiresIn'], str)
    testcase.assertAlmostEqual(int(resp_data['refreshTokenExpiresIn']), 63071999, delta=500)  # 2 years
    testcase.assertIsInstance(resp_data['refreshTokenIssuedAt'], str)
    testcase.assertAlmostEqual(int(resp_data['refreshTokenIssuedAt'])/1000, time.time(), delta=10)


def different_clients_than(device):
    """Generator that yields tuples of (device, device_data) for all devices in
    device_data that have a different value of field `client` then specified in
    parameter `device`.
    """
    yielded_clients = {devices[device]['client'], ''}
    for device, device_data in devices.items():
        if device_data['client'] not in yielded_clients:
            yielded_clients.add(device_data['client'])
            yield device, device_data


class CheckDeviceData(TestCase):
    def test_api_key(self):
        """Test if devices with the same client ID have the same API key and platform"""
        api_key_map = {}
        platform_map = {}
        for device, dev_data in devices.items():
            api_key = api_key_map.setdefault(dev_data['client'], dev_data['api_key'])
            self.assertEqual(api_key, dev_data['api_key'],
                             f'Device "{device}" has a different API key than other devices of its kind.')
            platform = platform_map.setdefault(dev_data['client'], dev_data['platform'])
            self.assertEqual(platform, dev_data['platform'],
                             f'Device "{device}" has a different platform than other devices of its kind.')


class CompareEntryPoints(TestCase):
    def test_compare_google_and_freeview_domain(self):
        freeview_resp = requests.get(
            'https://freeview.bsd.client.streaming.channel4.com/webapp/index.html',
            headers=api_auth_headers(DEVICE, hdr_fields={'authorization': None})
        )
        google_resp = requests.get(
            'https://google.bsd.client.streaming.channel4.com/webapp/index.html',
            headers=api_auth_headers(DEVICE, hdr_fields={'authorization': None})
        )
        self.assertNotEqual(freeview_resp.text, google_resp.text)
        # The only differences are the versions of static/js/main.xxxxx.js and
        # static/js/runtime-main.xxxx.js.
        # Remove the version strings and test if they are now the same.
        pattern = re.compile(r'(static/js/(?:runtime-)?main\.)([^.]+\.)(chunk|js)')
        freeview_html = pattern.sub(r'\1\3', freeview_resp.text)
        google_html = pattern.sub(r'\1\3', google_resp.text)
        self.assertEqual(freeview_html, google_html)


class TestWebLogin(TestCase):
    def test_recaptcha(self):
        resp = requests.get(
            url='https://www.channel4.com/sign-in-or-register',
            headers={
                'user-agent': WEB_USER_AGENT,
                'accept-language': 'en-GB,en;q=0.5',
                'origin': 'https://www.channel4.com',
                'sec-fetch-site': 'same-origin',
                'referer': 'https://www.channel4.com/',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-dest': 'document',
            }
        )
        site_key = re.search(r'"siteKey":"(\w+)",', resp.text)
        self.assertTrue(site_key)

        resp = requests.post(
            url='https://www.google.com/recaptcha/enterprise/reload?k=' + site_key[0],
            headers={
                'user-agent': WEB_USER_AGENT,
                'accept-language': 'en-GB,en;q=0.5',
                'origin': 'https://www.google.com',
                'referer': ('https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Leyk3gbAAAAAFXvdqcW04M6tVBCBxkn'
                            '2u4176Js&co=aHR0cHM6Ly93d3cuY2hhbm5lbDQuY29tOjQ0Mw..&hl=en&v=U5VsmTDhJM1iOJUyw4DEUTYv&size'
                            '=invisible&anchor-ms=20000&execute-ms=30000&cb=d4cgz5olg2uz_GRECAPTCHA=09AKhCRwhzPEpWhAzqf'
                            'SakVksWIkDcb-ND38_qIW6K5dqasoQSCJmJdzNuZ-mlo399pEOv4u5vmcBUZAN91S7NI7I'),
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
            }

        )

    def test_login(self):
        with requests.Session() as sess:
            sess.headers = {
                'user-agent': WEB_USER_AGENT,
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
                    'user-agent': WEB_USER_AGENT,
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


def api_auth_headers(device,
                     hdr_fields: dict | None = None):
    headers = {
        'user_agent': devices[device]['user_agent'],
        'authorization': 'Basic ' + devices[device]['api_key'],
        'origin': 'https://google.bsd.client.streaming.channel4.com',
        'referer': 'https://google.bsd.client.streaming.channel4.com/',
    }
    if hdr_fields:
        # Update case-insensitive
        headers.update({k.lower(): v for k, v in hdr_fields.items()})
    # Allow callers to delete default headers by setting their value to None
    return {k: v for k, v in headers.items() if v is not None}


def api_login(uname: str,
              passw: str,
              device: str = 'amazon-fos8',
              headers: dict | None = None,
              params: dict | None = None):

    auth_headers = api_auth_headers(device, headers)

    dflt_params = {'client': devices[device]['client']}
    if params:
        dflt_params.update(params)

    resp = requests.post(
        url='https://api.channel4.com/online/v2/auth/token',
        headers=auth_headers,
        params=dflt_params,
        data={'username': uname,
              'password': passw,
              'grant_type': 'password'}
    )
    return resp


class APILogin(TestCase):
    DEVICE_TYPE = 'amazon-fos8'

    def login(self,
              uname: str,
              passw: str,
              device: str | None = None,
              headers: dict | None = None,
              params: dict | None = None):
        if device is None:
            device = self.DEVICE_TYPE
        return api_login(uname, passw, device, headers, params)

    def test_login_valid_credentials(self):
        """Login at the API end point with username and password.

        The tokens returned appear to be for a specific client type only. Using them
        in conjunction with another type at some API end points may (or will) result
        in 401 errors.

        The looks like the client type is defined by the auth header in the login request.
        The querystring argument 'client' does not seem to have any effect and could
        even be omitted.

        There's currently no geo-block on login requests.

        """
        resp = self.login(UNAME, PASSW)
        self.assertEqual(200, resp.status_code)
        check_auth_data(self, resp.json())

    def test_loging_without_api_key(self):
        resp = self.login(UNAME, PASSW, headers={'Authorization': None})
        self.assertEqual(401, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(473, resp_data['errorCode'])
        self.assertEqual('client_credentials_are_not_provided', resp_data['error'])

    def test_login_with_wrong_username(self):
        # username is not an email address
        resp = self.login('sfhsdbf', PASSW)
        self.assertEqual(400, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(10002, resp_data['errorCode'])
        self.assertEqual('invalid_request', resp_data['error'])
        self.assertEqual('Request parameter error', resp_data['errorMessage'])

        # username is a non-existing, but otherwise valid email address
        resp = self.login('sfhsdbf@sipolifo.com', PASSW)
        self.assertEqual(400, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(210, resp_data['errorCode'])
        self.assertEqual('identity_invalid_credentials', resp_data['error'])
        self.assertEqual('The username/password combination supplied was incorrect', resp_data['errorMessage'])

    def test_login_with_wrong_password(self):
        resp = self.login(UNAME, 'zdgsdgfv')
        self.assertEqual(400, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(210, resp_data['errorCode'])
        self.assertEqual('identity_invalid_credentials', resp_data['error'])
        self.assertEqual('The username/password combination supplied was incorrect', resp_data['errorMessage'])

    def test_login_with_invalid_api_key(self):
        # Auth header not matching any known device.
        headers = {'authorization': 'Basic eUNFVEVrelV4ZUNzcDJabltUJJbkg5b1223PbFh6b0xtMzk6UTgxd01kSEcyNahFTV6xNg=='}
        resp = self.login(UNAME, PASSW, headers=headers)
        self.assertEqual(401, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(401, resp_data['errorCode'])
        self.assertEqual('invalid_api_key', resp_data['error'])
        self.assertEqual('The API key is invalid.', resp_data['errorMessage'])

    def test_login_with_api_key_not_matching_client(self):
        """Test login with an API key of a different device than specified  as
        `device` in the query string.

        """
        params = {'client': devices['freeview-hp']['client']}
        resp = self.login(UNAME, PASSW, device='amazon-fos8', params=params)
        self.assertEqual(200, resp.status_code)
        check_auth_data(self, resp.json())


class APiRefreshTokens(TestCase):
    DEVICE_TYPE = 'amazon-fos8'

    @staticmethod
    def refresh(device: str,
                refresh_token: str,
                headers: dict[str, str | None] | None = None,
                params: dict[str, str] | None = None):

        auth_headers = api_auth_headers(device, headers)
        dflt_params = {'client': devices[device]['client']}
        if params:
            dflt_params.update(params)

        resp = requests.post(
            url='https://api.channel4.com/online/v2/auth/token',
            headers=auth_headers,
            params=dflt_params,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        )
        return resp

    def test_refresh_valid_token(self):
        auth_data = api_login(UNAME, PASSW, self.DEVICE_TYPE).json()
        resp = self.refresh(self.DEVICE_TYPE, auth_data['refreshToken'])
        self.assertEqual(200, resp.status_code)
        check_auth_data(self, resp.json())

    def test_refresh_a_totally_invalid_token(self):
        resp = self.refresh(self.DEVICE_TYPE, 'dvkt5d8gjc6554eHyx678dfg')
        self.assertEqual(401, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(462, resp_data['errorCode'])
        self.assertEqual('invalid_refresh_token', resp_data['error'])

    def test_refresh_without_api_key(self):
        ensure_signed_in()
        resp = self.refresh(self.DEVICE_TYPE, TOKENS[DEVICE]['refreshToken'], headers={'authorization': None})
        self.assertEqual(401, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(473, resp_data['errorCode'])
        self.assertEqual('client_credentials_are_not_provided', resp_data['error'])

    def test_re_use_a_refresh_token(self):
        auth_data = api_login(UNAME, PASSW, self.DEVICE_TYPE).json()
        resp = self.refresh(self.DEVICE_TYPE, auth_data['refreshToken'])
        self.assertEqual(200, resp.status_code)
        time.sleep(5)
        # Refresh again using the same token
        resp = self.refresh(self.DEVICE_TYPE, auth_data['refreshToken'])
        self.assertEqual(200, resp.status_code)

    def test_refresh_valid_token_with_another_device(self):
        ensure_signed_in()
        refr_tkn = TOKENS[DEVICE]['refreshToken']
        for device_type, device_data in different_clients_than(DEVICE):
            resp = self.refresh(device_type, refr_tkn)
            self.assertEqual(401, resp.status_code)
            resp_data = resp.json()
            self.assertEqual(401, resp_data['errorCode'])
            self.assertEqual('invalid_refresh_token_client_id', resp_data['error'])


class ApiLogOut(TestCase):
    @staticmethod
    def logout(refr_tkn, device: str | None = None):
        """This is what the apps do when the user logs out."""
        if device is None:
            device = DEVICE
        return requests.post(
            url='https://api.channel4.com/online/v2/auth/revoke',
            headers=api_auth_headers(device),
            data={'token_type_hint': 'refresh_token',
                  'token': refr_tkn,
                  'grant_type': 'refresh_token'},
            # params={'client': 'fvp'}
        )

    def test_logout_with_valid_token(self):
        auth_data = api_login(UNAME, PASSW).json()
        refr_tkn = auth_data['refreshToken']
        resp = self.logout(refr_tkn)
        self.assertEqual(200, resp.status_code)
        self.assertFalse(resp.content)

        # log out with an already revoked token.
        resp = self.logout(refr_tkn)
        self.assertEqual(401, resp.status_code)
        resp_data = json.loads(resp.content)
        self.assertEqual(469, resp_data['errorCode'])
        self.assertEqual(resp_data['error'], 'revoked_refresh_token',)

    def test_logout_as_different_device(self):
        """Perform log out authenticated as a device different to the one
        used to log in.

        """
        auth_data = api_login(UNAME, PASSW, 'amazon-fos8').json()
        refr_tkn = auth_data['refreshToken']

        resp = self.logout(refr_tkn, 'freeview-hp')
        self.assertEqual(401, resp.status_code)
        resp_data = json.loads(resp.content)
        self.assertEqual(401, resp_data['errorCode'])
        self.assertEqual(resp_data['error'], 'invalid_refresh_token_client_id')

    def test_logout_with_invalid_token(self):
        # Just a rondom string of characters.
        resp = self.logout('kdfjhlsdfmlsmdlfkjslfk')
        self.assertEqual(401, resp.status_code)
        resp_data = json.loads(resp.content)
        self.assertEqual(462, resp_data['errorCode'])
        self.assertEqual(resp_data['error'], 'invalid_refresh_token', )


class TvPairing(TestCase):
    def get_pin(self, device):
        resp = requests.get(
            'https://api.channel4.com/online/v2/auth/pin',
            headers=api_auth_headers(device)
        )
        self.assertEqual(resp.status_code, 200)
        resp_data = resp.json()
        self.assertTrue('userCode' in resp_data)
        self.assertTrue('deviceCode' in resp_data)
        self.assertEqual(resp_data['expiresIn'], 600)
        self.assertEqual(resp_data['nextPollIn'], 5)
        self.assertEqual(resp_data['verification']['url'], 'channel4.com/code')
        create_date = datetime.strptime(resp_data['createDate'], '%Y-%m-%d %H:%M:%S %z')
        self.assertAlmostEqual(create_date, datetime.now(tz=timezone.utc), delta=timedelta(seconds=10))
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
            check_auth_data(self, resp_data)

    def test_get_pin(self):
        self.get_pin(DEVICE)


class ApiPLayList(TestCase):
    PROGRAMME_ID = '76930-063'           # Hollyoaks, mon 1 jun 2026

    def setUp(self):
        ensure_signed_in()

    def request_playlist(self,
                         auth_key: str,
                         progr_id: str | None = None,
                         device: str | None = None,
                         headers: dict[str, str | None] | None = None,
                         params: dict[str, str] | None = None) -> requests.Response:
        if progr_id is None:
            progr_id = self.PROGRAMME_ID
        if device is None:
            device = DEVICE

        auth_headers = {'Authorization': 'Bearer ' + auth_key}
        if headers:
            auth_headers.update(headers)
        headers = api_auth_headers(device, auth_headers)
        dflt_params = {'client': devices[device]['client']}
        if params:
            dflt_params.update(params)
        resp = requests.get(f'https://api.channel4.com/online/v1/vod/stream/{progr_id}',
                            headers=headers,
                            params=dflt_params)
        return resp

    def test_get_playlist(self):
        access_token = TOKENS[DEVICE]['accessToken']

        resp = self.request_playlist(access_token, params={'uuid': TOKENS[DEVICE]['user']['uuid']})
        # Requests originating from a non-residential IP address may get geo-blocked.
        # Accept the 403 status code as a valid response.
        self.assertTrue(resp.status_code in (200, 403))
        resp_data = resp.json()
        if resp.status_code == 200:
            check_playlist(self, resp_data)
        else:
            self.assertEqual(10302, resp_data['code'])
            self.assertEqual('This programme is not available in your current location.', resp_data['description'])

    def test_get_playlist_with_full_headers(self):
        """Test requests with all headers a browser uses.

        Tests from my location all return a 403 geo-block, and sending all headers doesn't change anything.
        If, and how it affects normal responses remains to be tested.
        """

        device = 'freeview-hp'
        ensure_signed_in(device)
        tz_uk = ZoneInfo('Europe/London')
        uk_now = datetime.now(tz=tz_uk).strftime('%Y-%m-%dT%H%M%S%z')
        access_token = TOKENS[device]['accessToken']

        headers = {
            'Accept-Language':           'en-GB,en;q=0.9',
            'Accept-Encoding':           'gzip, deflate, br, zstd',
            'X-C4-Date':                 ':'.join((uk_now[:-2], uk_now[-2:])),
            'X-C4-Platform-Name':        devices[device]['platform'],
            # not sure if this makes sense on anything other than freeview
            'X-C4-App-Version':          devices[device]['platform'] + '_app:26.2.0',
            'X-C4-Device-Name':          'mb181',
            'X-C4-Device-Type':          'tv',
            'X-C4-Optimizely-Datafile':  'unknown',
            'X-Correlation-Id':          'BSD-' + str(uuid4()),
            'Origin':                    'https://google.bsd.client.streaming.channel4.com',
            'Connection':                'keep-alive',
            'Referer':                   'https://google.bsd.client.streaming.channel4.com/',
            'Sec-Fetch-Dest':            'empty',
            'Sec-Fetch-Mode':            'cors',
            'Sec-Fetch-Site':            'same-site',
            'sec-ch-ua-platform':        '"Linux"',
            'sec-ch-ua':                 '"(Not(A:Brand";v="8", "Chromium";v="98"',
            'sec-ch-ua-mobile':          '?0',
            'Priority':                  'u=0',
            'Pragma':                    'no-cache',
            'Cache-Control':             'no-cache',
        }

        resp = self.request_playlist(access_token,
                                     device=device,
                                     headers=headers,
                                     params={'uuid': TOKENS[device]['user']['uuid']})
        self.assertEqual(200, resp.status_code)
        resp_data = resp.json()
        check_playlist(self, resp_data)

    def test_get_playlist_without_uuid(self):
        """The original TV apps send the user's uuid with the playlist request.
        Check that this is not really necessary.
        """
        access_token = TOKENS[DEVICE]['accessToken']

        resp = self.request_playlist(access_token)
        self.assertEqual(200, resp.status_code)
        check_playlist(self, resp.json())

    def test_request_playlist_from_a_different_device(self):
        """Request the playlist with a device specified in the querystring that is different
        to the one used to log in.

        """
        access_token = TOKENS[DEVICE]['accessToken']
        for device, _ in different_clients_than(DEVICE):
            resp = self.request_playlist(access_token, device=device)
            self.assertEqual(401, resp.status_code)
            resp_data = resp.json()
            self.assertEqual(10302, resp_data['code'])
            self.assertEqual('This programme is not available in your current location.', resp_data['description'])


def check_playlist(testcase: TestCase, data: dict):
    testcase.assertGreater(data['duration'], 0)
    testcase.assertEqual('HD', data['resolution'])
    testcase.assertTrue(data['audioDescription']['isAudioDescribed'])
    testcase.assertEqual(1, len(data['audioDescription']))          # just to flag when more data becomes available.
    testcase.assertGreater(data['endCredits']['squeezeIn'], 0)
    testcase.assertEqual(2, len(data['endCredits']))                # just to flag when more data becomes available.
    subtitles = data['subtitlesAssets']
    testcase.assertIsInstance(subtitles, list)
    for sub in subtitles:
        testcase.assertTrue(sub['format'] in ('webvtt_003', 'webvtt_007', 'srt_009', 'sami_001'))
        testcase.assertTrue(sub['url'].startswith('https://'))
    video_profiles = data['videoProfiles']
    testcase.assertIsInstance(video_profiles, list)
    for profile in video_profiles:
        testcase.assertEqual(1, len(profile['streams']))
        for strm in profile['streams']:
            testcase.assertTrue(strm['uri'].startswith('https://'))
            testcase.assertIsInstance(strm['token'], str)
            testcase.assertGreater(len(strm['token']), 32)
        testcase.assertIsInstance(profile['name'], str)
    testcase.assertIsInstance(data['skipIntro'], dict)


class WebPLayList(TestCase):
    PROGRAMME_ID = '76930-063'           # Hollyoaks, mon 1 jun 2026

    def test_request_playlist(self):
        resp = requests.get(f'https://www.channel4.com/vod/stream/{self.PROGRAMME_ID}',
                            headers={'user-agent': WEB_USER_AGENT})
        self.assertEqual(200, resp.status_code)
        check_playlist(self, resp.json())


class WebCategories(TestCase):
    def test_category_default_page_size(self):
        resp = requests.get('https://www.channel4.com/categories/drama?sort=az&json=true')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreater(data['noOfShows'], 300)
        self.assertTrue('pageTitle' in data)
        self.assertTrue('baseUrl' in data)
        self.assertFalse(data['user']['authenticated'])
        items = data['brands']['items']
        self.assertEqual(60, len(items))

    def test_category_page_size(self):
        """Test the effect of parameter `limit`

        Does not seem to have any effect.
        """
        resp = requests.get('https://www.channel4.com/categories/drama?sort=az&json=true&limit=400')
        data = resp.json()
        self.assertEqual(60, len(data['brands']['items']))
        resp = requests.get('https://www.channel4.com/categories/drama?sort=az&json=true&offset=120&limit=20')
        data = resp.json()
        self.assertEqual(60, len(data['brands']['items']))


class ApiMy4Access(TestCase):
    """
    To obtain My4 the request has to be authenticated with a valid accessToken.
    It doesn't seem to matter much which client is passed on in the query string,
    as long as it is a known client.
    """
    MY4_URL = 'https://api.channel4.com/online/v1/views/my4.json'

    def setUp(self):
        ensure_signed_in()

    def check_my4_data(self, resp_data: dict):
        self.assertTrue(True, resp_data['user']['authenticated'])
        self.assertIsInstance(resp_data['sliceGroups'], list)
        self.assertEqual(1, len(resp_data['sliceGroups']))
        slice_grp = resp_data['sliceGroups'][0]
        self.assertEqual('My4', slice_grp['title'])
        slice_types = [s['type'] for s in slice_grp['slices']]
        self.assertTrue('CONTINUE_WATCHING' in slice_types)
        self.assertTrue('MYLIST' in slice_types)
        self.assertTrue('REMINDERS' in slice_types)
        self.assertTrue('HISTORY' in slice_types)
        self.assertTrue('RECOMMENDATIONS' in slice_types)

    def test_get_my4(self):
        """Request my4 data in very much the same way as apps do."""
        headers = api_auth_headers(DEVICE, {'authorization': 'Bearer ' + TOKENS[DEVICE]['accessToken']})
        resp = requests.get(self.MY4_URL,
                            headers=headers,
                            params={'client': devices[DEVICE]['client']})
        self.assertEqual(200, resp.status_code)
        resp_data = resp.json()
        self.check_my4_data(resp_data)

    def test_my4_without_being_logged_in(self):
        headers = api_auth_headers(DEVICE, {'authorization': None})
        resp = requests.get(self.MY4_URL,
                            headers=headers,
                            params={'client': devices[DEVICE]['client']})
        self.assertEqual(401, resp.status_code)
        resp_data = resp.json()
        # Note: This data structure differs from login/refresh errors.
        self.assertEqual('oauth.v2.InvalidAccessToken', resp_data['fault']['detail']['errorcode'])
        self.assertEqual('Invalid access token', resp_data['fault']['faultstring'])

    def test_get_my4_with_different_client(self):
        """Request my4 with a client in the querystring that differs from the
        client used to log in.
        """
        headers = api_auth_headers(DEVICE, {'authorization': 'Bearer ' + TOKENS[DEVICE]['accessToken']})
        for client in allowed_clients:
            if client == devices[DEVICE]['client']:
                continue
            resp = requests.get(self.MY4_URL,
                                headers=headers,
                                params={'client': client})
            self.assertEqual(200, resp.status_code)
            resp_data = resp.json()
            self.check_my4_data(resp_data)

    def test_get_my4_without_client(self):
        """Request my4 without specifying a client in the querystring.
        """
        headers = api_auth_headers(DEVICE, {'authorization': 'Bearer ' + TOKENS[DEVICE]['accessToken']})
        resp = requests.get(self.MY4_URL,
                            headers=headers)
        self.assertEqual(400, resp.status_code)
        resp_data = resp.json()
        # Note: Unlike the error without being logged in, this data structure is more
        # like login/refresh errors, but still not quite the same.
        self.assertEqual(400, resp_data['code'])
        self.assertEqual("The required parameters \'Client ID\' was not provided", resp_data['message'])

    def test_get_my4_with_invalid_client(self):
        """Request my4 without specifying a client in the querystring not known to channel4.
        """
        headers = api_auth_headers(DEVICE, {'authorization': 'Bearer ' + TOKENS[DEVICE]['accessToken']})
        resp = requests.get(self.MY4_URL,
                            headers=headers,
                            params={'client': 'unknown'})
        self.assertEqual(400, resp.status_code)
        resp_data = resp.json()
        self.assertEqual(400, resp_data['code'])
        self.assertTrue("Missing or wrong mandatory query parameter \'client\'." in resp_data['message'])

    def test_get_my4_with_different_client_and_different_user_agent(self):
        """Request my4 with both a different client than the one used to log in, and with
         a different user-agent.
        """
        headers = {
            'user-agent': WEB_USER_AGENT,
            'authorization': 'Bearer ' + TOKENS[DEVICE]['accessToken']}
        auth_client = devices[DEVICE]['client']
        client = 'fvp' if auth_client != 'fvp' else 'amazonfire-dash'
        resp = requests.get(self.MY4_URL,
                            headers=headers,
                            params={'client': client})
        self.assertEqual(200, resp.status_code)
        resp_data = resp.json()
        self.check_my4_data(resp_data)


class ApiMy4lLists(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__my4_data = None

    def my4_data(self):
        if self.__my4_data is None:
            resp = requests.get(
                'https://api.channel4.com/online/v1/views/my4.json',
                headers=api_auth_headers(DEVICE, {'authorization': 'Bearer ' + TOKENS[DEVICE]['accessToken']}),
                params={'client': devices[DEVICE]['client']}
            )
            self.assertEqual(200, resp.status_code)
            self.__my4_data = resp.json()
        return self.__my4_data

    def get_my4_slice(self, slice_type):
        data = self.my4_data()
        for data_slice in data['sliceGroups'][0]['slices']:
            if data_slice['type'] == slice_type:
                return data_slice
        else:
            raise ValueError(f'Unknown slice of type {slice_type}')

    def test_my_four(self):
        data = self.my4_data()
        slices = data['sliceGroups'][0]['slices']
        slice_types = [s['type'] for s in slices]
        self.assertTrue('CONTINUE_WATCHING' in slice_types)
        self.assertTrue('MYLIST' in slice_types)
        self.assertTrue('REMINDERS' in slice_types)
        self.assertTrue('HISTORY' in slice_types)
        self.assertTrue('RECOMMENDATIONS' in slice_types)

    def test_watching(self):
        watching = self.get_my4_slice('CONTINUE_WATCHING')
        for item in watching['sliceItems'][1:]:
            self.assertTrue('title' in item)
            self.assertTrue('summary' in item)
            self.assertTrue('secondaryTitle' in item)
            self.assertTrue(item['image']['href'].startswith("https://"))
            self.assertTrue('websafeTitle' in item['brand'])
            self.assertTrue('ondemandSeriesCount' in item['brand'])
            self.assertTrue('ondemandEpisodesCount' in item['brand'])

            self.assertTrue('title' in item['episode'])
            self.assertTrue('secondaryTitle' in item['episode'])
            self.assertTrue('episodeNumber' in item['episode'])
            self.assertTrue('seriesNumber' in item['episode'])
            self.assertTrue('summary' in item['episode'])
            # self.assertTrue('firstTXDate' in item['episode'])
            self.assertTrue('newEpisode' in item['episode'])
            self.assertTrue('nextEpisode' in item['episode'])

            resume_info = item['episode']['resume']
            self.assertTrue('lastModified' in resume_info)
            self.assertTrue('seconds' in resume_info)
            self.assertTrue('completed' in resume_info)

            stream_info = item['episode']['assetInfo']['streaming']
            self.assertTrue('assetId' in stream_info)
            self.assertTrue('duration' in stream_info)
            self.assertTrue('endDate' in stream_info)
            self.assertTrue('href' in stream_info)
            self.assertTrue('vodBSHref' in stream_info)
            self.assertTrue('subtitles' in stream_info)


class MyListEdit(TestCase):
    """Add to and remove from My List"""

    def test_add_remove_to_mylist(self):
        headers = api_auth_headers(DEVICE, {'authorization': 'Bearer ' + TOKENS[DEVICE]['accessToken']})
        # corresponding web url: https://www.channel4.com/my4/api/v1/user/favourites/elementary
        url = 'https://api.channel4.com/online/v1/user/favourites/elementary.json?client=amazonfire-dash'
        # ensure the item is not on the list
        requests.delete(url, headers=headers)

        # Add the item to the list
        # Yep, a post without content...
        resp = requests.post(url, headers=headers)
        self.assertEqual(200, resp.status_code)
        resp_data = resp.json()
        self.assertAlmostEqual(resp_data['createdDate']/1000, time.time(), delta=10)

        # Add an item already on the list.
        resp = requests.post(url, headers=headers)
        self.assertEqual(200, resp.status_code)

        # Remove an item that is actually on the list.
        resp = requests.delete(url, headers=headers)
        self.assertEqual(200, resp.status_code)
        self.assertEqual('', resp.text)     # no content

        # Remove an item that is noton the list.
        resp = requests.delete(url, headers=headers)
        self.assertEqual(200, resp.status_code)
        self.assertEqual('', resp.text)     # no content


class ReportPlayTime(TestCase):
    def setUp(self):
        ensure_signed_in()

    def test_report_playtime_web(self):
        resp = requests.post(
            url='https://www.channel4.com/player/history/76930-028/300',     # Hollyoaks S01E28
            headers={
                'User-Agent': WEB_USER_AGENT,
                'accept-language': 'en-GB,en;q=0.5',
                # 'authorization': 'Bearer ' + TOKENS['accessToken'],
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty'},
            cookies={
                # insert access JWT
                'C4_AT': '<REDACTED>',
            },
            json={}
        )
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertEqual(data['message'], 'OK')

    def test_report_playtime_api(self):
        resp = requests.put(
            url='https://api.channel4.com/online/v1/user/history/76930-028/600.json',     # Hollyoaks S01E28
            headers={
                'User-Agent': devices[DEVICE]['user_agent'],
                'accept-language': 'en-GB,en;q=0.5',
                # 'X-C4-Platform-Name':        'freeview',
                # 'X-C4-App-Version':          'freeview_app:26.2.0',
                # 'X-C4-Device-Name':          'mb181',
                # 'X-C4-Device-Type':          'tv',
                # 'X-C4-Optimizely-Datafile':  'unknown',
                'authorization': 'Bearer ' + TOKENS['accessToken'],
                # 'X-Correlation-Id':          'BSD-' + str(uuid4()),
                # 'sec-fetch-site': 'same-site',
                # 'sec-fetch-mode': 'cors',
                # 'sec-fetch-dest': 'empty',
                # 'sec-ch-ua-platform':        '"Linux"',
                # 'sec-ch-ua':                 '"Not/A)Brand";v="8", "Chromium";v="46", "Opera";v="46"',
                # 'sec-ch-ua-mobile':          '?0',
                'Pragma':                    'no-cache',
                'Cache-Control':             'no-cache'
            },
            params={'client': devices[DEVICE]['client']},
            json={}
        )
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.content, b'')

    def test_report_playtime_with_invalid_video_id(self):
        resp = requests.put(
            url='https://api.channel4.com/online/v1/user/history/76930-925/600.json?client=fvp',
            headers={
                'User-Agent': devices[DEVICE]["user_agent"],
                'accept-language': 'en-GB,en;q=0.5',
                'authorization': 'Bearer ' + TOKENS['accessToken'],
                'Pragma':                    'no-cache',
                'Cache-Control':             'no-cache'
            },
            json={}
        )
        self.assertEqual(404, resp.status_code)
