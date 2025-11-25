import os
import time

from unittest import TestCase
from unittest.mock import patch, MagicMock

from codequick import Listitem

from resources.lib.channels.uk import uktvplay

from testutils import open_doc, HttpResponse


docs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs')


class MainPage(TestCase):
    @patch('urlquick.get',
           return_value=HttpResponse(200, text=open_doc('index.html', docs_dir)))
    def test_collections(self, _):
        li_items = list(uktvplay.list_collections.test())
        self.assertGreater(len(li_items), 5)
        for li in li_items:
            self.assertIsInstance(li, Listitem)