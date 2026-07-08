from __future__ import annotations
import os
import json
from unittest.mock import patch

import urlquick


patch_1 = None


class RealWebRequestMadeError(Exception):
    pass


def setup_local_tests():
    """Module level fixture for all local tests. Ensures that no unintentional real
    web requests can occur.

    """
    global patch_1
    patch_1 = patch('requests.sessions.Session.send', side_effect=RealWebRequestMadeError)
    patch_1.start()


def tear_down_local_tests():
    global patch_1

    if patch_1:
        patch_1.stop()
        patch_1 = None


def open_doc(file_name: str, base_path: str = ''):
    fullpath = os.path.join(base_path, file_name)
    with open(fullpath, 'r') as f:
        return f.read()


def open_json(file_name: str, base_path: str = ''):
    data = open_doc(file_name, base_path)
    return json.loads(data)


class HttpResponse(urlquick.Response):
    """Create a urlquick.Response object with various attributes set.
    Can be used as the `return_value` of a mocked urlquick.request.

    """
    def __init__(self, status_code: int = None, headers: dict = None,
                 content: bytes = None, text: str = None, reason=None):
        super().__init__()
        if status_code is not None:
            self.status_code = status_code
        if headers is not None:
            for k, v in headers.items():
                self.headers[k] = v
        if reason is not None:
            self.reason = reason
        if content is not None:
            self._content = content
            if status_code is None:
                self.status_code = 200
                self.reason = 'OK'
        elif text is not None:
            self._content = text.encode('utf8')
            if status_code is None:
                self.status_code = 200
                self.reason = 'OK'
