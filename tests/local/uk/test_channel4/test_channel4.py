
import os
import time

from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests
import xbmcvfs

from codequick import Listitem

from resources.lib.channels.uk import channel4

from testutils import (
    open_doc,
    HttpResponse,
    setup_local_tests,
    tear_down_local_tests
)

setUpModule = setup_local_tests
tearDownModule = tear_down_local_tests

my_dir = os.path.abspath(os.path.dirname(__file__))


def check_list_items(testcase: TestCase, items_list: list, count: int):
    testcase.assertEqual(count, len(items_list))
    testcase.assertTrue(all(isinstance(item, Listitem) for item in items_list),
                        "Not all items are Listitem objects.")


class LoadChannel4Auth(TestCase):
    def setUp(self):
        self.file_mock = MagicMock(name='file_mock', auto_spec=xbmcvfs.File)
        self.file_mock.__enter__ = MagicMock(return_value=self.file_mock)
        self._file_patch = patch('resources.lib.channels.uk.channel4.xbmcvfs.File', return_value=self.file_mock)
        self._file_patch.start()

    def tearDown(self):
        self._file_patch.stop()

    def test_load_valid_channel4_auth(self):
        self.file_mock.read.return_value = '{"accessToken":"my.access.tkn"}'
        result = channel4.load_channel4_auth()
        self.assertDictEqual({'accessToken': 'my.access.tkn'}, result)

    def test_auth_file_not_present(self):
        self.file_mock.read = MagicMock(side_effect=FileNotFoundError)
        result = channel4.load_channel4_auth()
        self.assertDictEqual({}, result)

    def test_auth_with_corrupted_non_json_file(self):
        # Should fail silently, regarded as file not present; i.e. not logged in.
        self.file_mock.read.return_value = 'my.access.tkn'
        result = channel4.load_channel4_auth()
        self.assertDictEqual({}, result)

    def test_auth_with_empty_file(self):
        # Should fail silently, same as corrupt json file.
        self.file_mock.read.return_value = ''
        result = channel4.load_channel4_auth()
        self.assertDictEqual({}, result)


@patch('codequick.Script.notify')
@patch('resources.lib.channels.uk.channel4.save_channel4_auth')
class Login(TestCase):
    @patch('requests.post', return_value=HttpResponse(content=b'{"accessToken": "NewTkn"}'))
    def test_login_succeeds(self, p_post, p_save, p_notify):
        result = channel4.login('my.email', 'my.password')
        self.assertEqual('NewTkn', result)
        p_post.assert_called_once()
        p_save.assert_called_once()
        p_notify.assert_not_called()

    @patch('requests.post', return_value=HttpResponse(
        content=b'{"error": "wrong params", "errorCode": 10002, "errorMessage": "some technical description"}'))
    def test_login_with_wrong_email(self, p_post, p_save, p_notify):
        """Error code 10002 is return when the provided email address is not a properly
        formatted email address, i.e. the address itself is invalid.

        """
        result = channel4.login('my.email', 'my.password')
        self.assertIsNone(result)
        p_post.assert_called_once()
        p_save.assert_not_called()
        self.assertEqual('Invalid email', p_notify.call_args.args[1])

    @patch('requests.post', return_value=HttpResponse(
        content=b'{"error": "wrong params", "errorCode": 210, "errorMessage": "wrong entry"}'))
    def test_login_with_invalid_credentials(self, p_post, p_save, p_notify):
        """Either the provided password is wrong or the email address is not registered.
        The user should get a notification with the error message from the backend.
        """
        result = channel4.login('my.email', 'my.password')
        self.assertIsNone(result)
        p_post.assert_called_once()
        p_save.assert_not_called()
        self.assertEqual('wrong entry', p_notify.call_args.args[1])

    @patch('requests.post', return_value=HttpResponse(
        status_code=403,
        content=b'{"error": {"description": "some failure or other"}}'))
    def test_login_with_different_json_response(self, p_post, p_save, p_notify):
        """The response is JOSN formatted, but tha data structure is not like we expect.
        This should just error out without notification (which will be handled by codequick).
        """
        self.assertRaises(requests.HTTPError, channel4.login, 'my.email', 'my.password')
        p_post.assert_called_once()
        p_save.assert_not_called()
        p_notify.assert_not_called()

    @patch('requests.post', return_value=HttpResponse(
        status_code=404,
        content=b'Not Found'))
    def test_login_error_without_json_formatted_body(self, p_post, p_save, p_notify):
        """This should just error out without notification (which will be handled by codequick).
        """
        self.assertRaises(requests.HTTPError, channel4.login, 'my.email', 'my.password')
        p_post.assert_called_once()
        p_save.assert_not_called()
        p_notify.assert_not_called()

    # Some corner case responses that will most likely never happen:

    @patch('requests.post', return_value=HttpResponse(content=b'yourKey = kjghmasdlkjdfmlk'))
    def test_login_success_without_json_response(self, p_post, p_save, p_notify):
        """The very remote chance that log in returns 200 OK, but its content is not JSON formatted.

        It doesn't really matter which, as long as an exception is raised, which will be logged with
        traceback by codequick.
        """
        self.assertRaises(Exception, channel4.login, 'my.email', 'my.password')
        p_post.assert_called_once()
        p_notify.assert_not_called()

    @patch('requests.post', return_value=HttpResponse(content=b'{"tokens": {"accessToken": "NewTkn"}}'))
    def test_login_success_wit_json_response_in_different_format(self, p_post, p_save, p_notify):
        """Log in returns 200 OK, but with a different data structure.

        It doesn't really matter which, as long as an exception is raised, which will be logged with
        traceback by codequick.
        """
        self.assertRaises(Exception, channel4.login, 'my.email', 'my.password')
        p_post.assert_called_once()
        p_notify.assert_not_called()


@patch('resources.lib.channels.uk.channel4.save_channel4_auth')
class Refresh(TestCase):
    @patch('requests.post', return_value=HttpResponse(content=b'{"accessToken": "NewTkn"}'))
    def test_successful_refresh(self, p_post, p_save):
        result = channel4.refresh('refttkn')
        self.assertEqual('NewTkn', result)
        p_post.assert_called_once()
        p_save.assert_called_once()

    @patch('requests.post', return_value=HttpResponse(
        status_code=401,
        content=b'{"error": "expired", "errorCode": "000", "errorMessage": "expired token"}'))
    def test_refresh_graceful_failure(self, p_post, p_save):
        # the service returns an error message
        with self.assertRaises(RuntimeError) as err_result:
            channel4.refresh('refttkn')
        self.assertTrue('expired token' in str(err_result.exception))
        self.assertTrue(getattr(err_result.exception, 'recoverable', None))
        p_post.assert_called_once()
        p_save.assert_not_called()

    @patch('requests.post', return_value=HttpResponse(status_code=404, reason=b'Not Found', content=b''))
    def test_refresh_with_other_http_errors(self, p_post, p_save):
        # The service returns an error without JSON formatted content
        with self.assertRaises(requests.HTTPError) as err_result:
            channel4.refresh('refttkn')
        self.assertTrue('Not Found' in str(err_result.exception))
        self.assertFalse(getattr(err_result.exception, 'recoverable', None))
        p_post.assert_called_once()
        p_save.assert_not_called()

    @patch('requests.post', side_effect=requests.ConnectionError)
    def test_refresh_with_non_http_errors(self, p_post, p_save):
        # The other errors should just bubble up.
        with self.assertRaises(requests.ConnectionError) as err_result:
            channel4.refresh('refttkn')
        self.assertFalse(getattr(err_result.exception, 'recoverable', None))
        p_post.assert_called_once()
        p_save.assert_not_called()

    # Some corner case responses that will most likely never happen:

    @patch('requests.post', return_value=HttpResponse(content=b'{"bla": "ajshdnank"}'))
    def test_refresh_no_access_token_in_response(self, p_post, _):
        # The web service returns no error, but lacks a field `accessToken` in the response
        # The type of error doesn't really matter, as long as it's not marked as recoverable.
        with self.assertRaises(Exception) as err_result:
            channel4.refresh('refttkn')
        self.assertFalse(getattr(err_result.exception, 'recoverable', None))
        p_post.assert_called_once()

    @patch('requests.post',  return_value=HttpResponse(status_code=200, content=b'some message'))
    def test_refresh_returns_non_json_200_response(self, p_post, p_save):
        """The remote chance that the web service returns a 200 OK response, but its content is not
        JSON formatted. This is a total change of API and is just an error as anything else.

        """
        # The type of error doesn't really matter, as long as it's not marked as recoverable.
        # It will always be a bit obscure, but logged with traceback by codequick.
        with self.assertRaises(Exception) as err_result:
            channel4.refresh('refttkn')
        self.assertFalse(getattr(err_result.exception, 'recoverable', None))
        p_post.assert_called_once()
        p_save.assert_not_called()


@patch('xbmcgui.Dialog.ok')
class GetAccessToken(TestCase):
    def setUp(self) -> None:
        try:
            # noinspection unresolved-references
            del channel4.get_access_token._channel4_auth
        except AttributeError:
            pass

    @patch('resources.lib.channels.uk.channel4.load_channel4_auth', return_value={})
    def test_get_access_token_not_logged_in(self, p_load_auth,  p_dlg):
        tkn = channel4.get_access_token(silent=True)
        self.assertIsNone(tkn)
        p_load_auth.assert_called_once()
        p_dlg.assert_not_called()

        # Not silent; should show an info dialog.
        tkn = channel4.get_access_token(silent=False)
        self.assertIsNone(tkn)
        p_dlg.assert_called_once()

    @patch('resources.lib.channels.uk.channel4.load_channel4_auth',
           return_value={'accessToken': 'SavedToken', 'issuedAt': str(int(time.time()*1000)), 'expiresIn': '600000'})
    def test_get_access_token_normal_logged_in(self, p_load_auth,  p_dlg):
        tkn = channel4.get_access_token(silent=False)
        self.assertEqual('SavedToken', tkn)
        p_load_auth.assert_called_once()
        p_dlg.assert_not_called()

    def test_access_token_refresh(self, p_dlg):
        expired_auth = {'accessToken': 'SavedToken',
                        'issuedAt': str(int(time.time() * 1000) - 2000),    # miliseconds
                        'expiresIn': '1',                                   # seconds
                        'refreshToken': 'MyRefrTkn'}

        with patch('resources.lib.channels.uk.channel4.refresh', return_value='NewAccessToken') as p_refresh:
            channel4.get_access_token._channel4_auth = expired_auth
            tkn = channel4.get_access_token(silent=False)
            self.assertEqual('NewAccessToken', tkn)
            p_refresh.assert_called_once()
            p_dlg.assert_not_called()

        # Refresh failed in a way that it is expected to be resolved by a re-login.
        # Should return None and open a dialog to ask the user to log in.
        p_dlg.reset_mock()
        err = RuntimeError("some msg")
        err.recoverable = True
        with patch('resources.lib.channels.uk.channel4.refresh', side_effect=err) as p_refresh:
            channel4.get_access_token._channel4_auth = expired_auth
            tkn = channel4.get_access_token(silent=False)
            self.assertIsNone(tkn)
            p_refresh.assert_called_once()
            p_dlg.assert_called_once()

        # Refresh encounters network error. Should *not* open a dialog to ask the user to log in,
        # but raise the error instead.
        p_dlg.reset_mock()
        with patch('resources.lib.channels.uk.channel4.refresh', side_effect=requests.ConnectionError) as p_refresh:
            channel4.get_access_token._channel4_auth = expired_auth
            self.assertRaises(requests.ConnectionError, channel4.get_access_token, silent=False)
            p_refresh.assert_called_once()
            p_dlg.assert_not_called()

    def test_get_access_token_errors_when_silent(self, p_dlg):
        """Any error should be dropped when silent is True"""
        with patch('resources.lib.channels.uk.channel4.load_channel4_auth',
                   side_effect=ValueError) as p_load_auth:
            self.assertIsNone(channel4.get_access_token(silent=True))
            p_load_auth.assert_called_once()

        # Malformed auth data
        channel4.get_access_token._channel4_auth = None
        with patch('resources.lib.channels.uk.channel4.load_channel4_auth',
                   return_value=['some', 'list']) as p_load_auth:
            self.assertIsNone(channel4.get_access_token(silent=True))
            p_load_auth.assert_called_once()

        # refresh failed with recoverable error
        err = RuntimeError("some msg")
        err.recoverable = True
        channel4.get_access_token._channel4_auth = {'refreshToken': 'dfgsgfs'}
        with patch('resources.lib.channels.uk.channel4.refresh', side_effect=err) as p_refresh:
            self.assertIsNone(channel4.get_access_token(silent=True))
            p_refresh.assert_called_once()

        # refresh fails with non-recoverable error
        for exc in (requests.ConnectionError, requests.HTTPError, RuntimeError):
            channel4.get_access_token._channel4_auth = {'refreshToken': 'dfgsgfs'}
            with patch('resources.lib.channels.uk.channel4.refresh', side_effect=exc) as p_refresh:
                self.assertIsNone(channel4.get_access_token(silent=True))
                p_refresh.assert_called_once()

        # Dialog should never have been called!
        p_dlg.assert_not_called()


class MainMenu(TestCase):
    @patch('urlquick.get', return_value=HttpResponse(text=open_doc('data/api_homepage.json', my_dir)))
    def test_list_main_menu(self, p_get):
        items = channel4.main_menu.test()
        p_get.assert_called_once()
        check_list_items(self, items, count=29)
        hero_items = [item for item in items
                      if '[B][COLOR orange]' in item.info['title'] and '[/COLOR][/B]' in item.info['title']]
        self.assertEqual(5, len(hero_items))

    @patch('urlquick.get', return_value=HttpResponse(text="Something that is not JSON"))
    def test_list_main_menu_with_home_page_error(self, p_get):
        """The whole homepage fails silently, leaving only the static items."""
        items = channel4.main_menu.test()
        p_get.assert_called_once()
        check_list_items(self, items, count=3)


@patch('resources.lib.channels.uk.channel4.authenticated_request',
       return_value=HttpResponse(text=open_doc('data/my4.json', my_dir)))
class MyListProgrammes(TestCase):
    def test_get_mylist_programmes_at_programme_start(self, p_request):
        # Ensure the state is like the start of the addon
        try:
            delattr(channel4.get_mylist_programmes, '_my_list_pgms')
        except AttributeError:
            pass
        pgm_list = channel4.get_mylist_programmes()
        p_request.assert_called_once()
        self.assertEqual(len(pgm_list), 6)

        # second request should come from cache
        p_request.reset_mock()
        pgm_list = channel4.get_mylist_programmes()
        p_request.assert_not_called()
        self.assertEqual(len(pgm_list), 6)

    def test_get_mylist_programmes_after_login(self, p_request):
        # clear the cache by assigning None, like login does.
        channel4.get_mylist_programmes._my_list_pgms = None
        pgm_list = channel4.get_mylist_programmes()
        p_request.assert_called_once()
        self.assertEqual(len(pgm_list), 6)

        # second request should come again from cache
        p_request.reset_mock()
        pgm_list = channel4.get_mylist_programmes()
        p_request.assert_not_called()
        self.assertEqual(len(pgm_list), 6)

    def test_get_mylist_programmes_after_logout(self, p_request):
        # Clear the cache by assigning False, like login does.
        # False indicates the user is not signed in, so no request will
        # be made to the backend.
        channel4.get_mylist_programmes._my_list_pgms = False
        pgm_list = channel4.get_mylist_programmes()
        p_request.assert_not_called()
        self.assertIs(pgm_list, False)


@patch('resources.lib.channels.uk.channel4.get_mylist_programmes', return_value=set())
class My4Lists(TestCase):
    @patch('urlquick.get')
    def test_sub_menu_my4(self, p_auth_req, _):
        items = channel4.submenu_my4.test()
        p_auth_req.assert_not_called()
        check_list_items(self, items, count=4)

    @patch('resources.lib.channels.uk.channel4.authenticated_request',
           return_value=HttpResponse(text=open_doc('data/my4.json', my_dir)))
    def test_get_mylist_logged_in(self, p_auth_req, _):
        items = channel4.list_my_four.test(list_type='CONTINUE_WATCHING')
        p_auth_req.assert_called_once()
        check_list_items(self, items, count=6)

    @patch('resources.lib.channels.uk.channel4.authenticated_request',
           return_value=HttpResponse(text=open_doc('data/my4.json', my_dir)))
    def test_list_my_list(self, p_auth_req, _):
        items = channel4.list_my_four.test('MYLIST')
        p_auth_req.assert_called_once()
        check_list_items(self, items, count=6)

    @patch('resources.lib.channels.uk.channel4.authenticated_request',
           return_value=HttpResponse(text=open_doc('data/my4.json', my_dir)))
    def test_list_history(self, p_auth_req, _):
        items = channel4.list_my_four.test('HISTORY')
        p_auth_req.assert_called_once()
        self.assertEqual(6, len(items))
        self.assertIsNone(items[1])   # Item is an episode that is no longer available.
        self.assertTrue(all(isinstance(item, Listitem) for item in items if items.index(item) != 1))

    @patch('resources.lib.channels.uk.channel4.authenticated_request',
           return_value=HttpResponse(text=open_doc('data/my4.json', my_dir)))
    def test_list_recommendations(self, p_auth_req, _):
        items = channel4.list_my_four.test('RECOMMENDATIONS')
        p_auth_req.assert_called_once()
        check_list_items(self, items, count=8)

    def test_empty_list(self, _):
        """Codequick always reports an empty list as a failure to Kodi.
        To work around this and just let Kodi display an actual empty list, we
        call endOfDirectory() ourselves and exit before codequick can interfere.

        """
        # This `freeform` item is always present, even on empty lists.
        list_data = {
            "title": "Watching",
            "type": "CONTINUE_WATCHING",
            "sliceItems": [
                {
                    "title": "",
                    "type": "freeform",
                    "summary": "Resume unfinished shows and see new available episodes",
                    "secondaryTitle": "",
                    "label": "",
                    "caption": ""
                },
            ],
        }
        with patch('resources.lib.channels.uk.channel4.get_my_four', return_value=list_data) as p_myfour:
            with patch('xbmcplugin.endOfDirectory') as p_end_dir:
                self.assertRaises(SystemExit, channel4.list_my_four.test, 'CONTINUE_WATCHING')
            p_myfour.assert_called_once()
            p_end_dir.assert_called_once_with(-1, True)

    @patch('resources.lib.channels.uk.channel4.authenticated_request',
           return_value=None)
    def test_not_authentitacted(self, p_auth_req, _):
        """The returned value should be False, or a list with a single item that
        is False, to explicitly indicate to codequick that the folder is empty.
        """
        items = channel4.list_my_four.test('RECOMMENDATIONS')
        p_auth_req.assert_called_once()
        self.assertListEqual([False], items)
