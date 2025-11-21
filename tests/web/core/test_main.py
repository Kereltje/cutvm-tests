
from unittest import TestCase
from unittest.mock import patch

import resources.lib.kodi_utils

patches = []


# def setUpModule():
#     patches.append(patch('resources.lib.kodi_utils.get_proxy', return_value=None))
#     for p in patches:
#         p.apply()

resources.lib.kodi_utils.get_proxy = lambda: None

from resources.lib import main

main.xbmc.getRegion = lambda x: '%H:%M' if x == 'time' else ''


class LiveWithGuide(TestCase):
    def test_live_uk_menu_with_guide(self):
        results = main.tv_guide_menu.test('uk_live')
        pass

    def test_live_fr_menu_with_guide(self):
        results = main.tv_guide_menu.test('fr_live')
        pass