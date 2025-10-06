

import os
import json

import urlquick


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
