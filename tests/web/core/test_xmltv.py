
import timeit
import datetime

from functools import partial
from datetime import timezone

from unittest import TestCase
from unittest.mock import patch, Mock

from resources.lib import xmltv


class GrabProgrammes(TestCase):
    # @patch.dict(xmltv.xmltv_infos['uk_live'],
    #             {'url': 'http://127.0.0.1:8083/tv_guide_uk_{}.xml',
    #             'md5_url': 'http://127.0.0.1:8083/tv_guide_uk_{}_md5.txt'})
    def test_grab_uk(self):
        result = xmltv.grab_programmes('uk_live', 0)
        self.assertIsInstance(result, list)

    def test_grab_uk_current_programmes(self):
        result = xmltv.grab_current_programmes('uk_live', 6)
        self.assertIsInstance(result, dict)

    def test_grab_fr_current_programmes(self):
        result = xmltv.grab_current_programmes('fr_live', 6)
        self.assertIsInstance(result, dict)

    def test_read_current_programmes(self):
        test_time = datetime.datetime.now(tz=timezone.utc).replace(hour=23, minute=15)
        with patch.object(datetime, 'datetime', Mock(wraps=datetime.datetime)) as patched_dt:
            patched_dt.now.return_value = test_time
            result = xmltv.grab_current_programmes('uk_live')
        for r in result:
            print(r)
        pass

    def test_grab_performance(self):
        test_time = datetime.datetime.now(tz=timezone.utc).replace(hour=22, minute=15)
        with patch.object(datetime, 'datetime', Mock(wraps=datetime.datetime)) as patched_dt:
            patched_dt.now.return_value = test_time
            t = min(timeit.Timer(partial(xmltv.grab_current_programmes, 'uk_live')).repeat(repeat=3, number=100))
            print(f"min grab time over 100 attempt: {t}")

    def test_read_programmes_performance(self):
        test_time = datetime.datetime.now(tz=timezone.utc).replace(hour=16, minute=15)
        with patch.object(datetime, 'datetime', Mock(wraps=datetime.datetime)) as patched_dt:
            patched_dt.now.return_value = test_time
            file_path = xmltv.get_xmltv_filepath('uk_live')
            func = partial(xmltv.read_current_programmes, file_path, 6)
            t = min(timeit.Timer(func).repeat(repeat=10, number=100))
            print(f"min read time over 100 attempt: {t}")
