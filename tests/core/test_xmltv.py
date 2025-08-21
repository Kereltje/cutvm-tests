
from unittest import TestCase
from unittest.mock import patch, MagicMock

from resources.lib import xmltv



class GrabProgrammes(TestCase):
    @patch.dict(xmltv.xmltv_infos['uk_live'],
                {'url': 'http://127.0.0.1:8083/tv_guide_uk_{}.xml',
                'md5_url': 'http://127.0.0.1:8083/tv_guide_uk_{}_md5.txt'})
    def test_grab_uk(self):
        result = xmltv.grab_programmes('uk_live', 0)
        self.assertIsInstance(result, list)