
from unittest import TestCase
from unittest.mock import patch

import resources.lib.kodi_utils
from resources.lib import iptvmanager


class TestIpTvMgr(TestCase):
    @patch('resources.lib.kodi_utils.get_setting', return_value=False)
    def test_get_channels(self, _):
        result = iptvmanager.get_all_live_tv_channels()
        pass

