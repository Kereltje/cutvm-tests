import requests
import re
import json

from unittest import TestCase

from credentials import credentials
from resources.lib.channels.uk import stv



class CategoryContent(TestCase):
    def check_programme(self, pgm):
        self.assertIsInstance(pgm['programme'], (str, type(None)))
        self.assertIsInstance(pgm['title'], str)
        self.assertIsInstance(pgm['description'], str)
        self.assertIsInstance(pgm['link'], str)
        self.assertTrue(pgm['link'].startswith('/'))
        self.assertIsInstance(pgm['guid'], str)
        self.assertIsInstance(pgm['playIcon'], bool)
        self.assertIsInstance(pgm['image'], dict)
        self.assertIsInstance(pgm['views'], int)
        self.assertIsInstance(pgm['type'], str)
        self.assertIsInstance(pgm['id'], str)
        self.assertEqual(len(pgm), 10)

    def test_api_content_entertainment(self):
        resp = requests.get(
            url=stv.URL_PROGRAMS_JSON,
            params={"category": 'entertainment',
                    "path": '/categories'}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        progrms = data["results"]
        pass

    def test_web_content_entertainment(self):
        resp = requests.get(
            url='https://player.stv.tv/categories/entertainment',
        )
        self.assertEqual(resp.status_code, 200)
        html = resp.text

        result = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html,
                           flags=re.DOTALL)
        json_str = result[1]
        data = json.loads(json_str)
        programmes = data['props']['pageProps']['data']['assets']
        pass

    def test_web_content_dramas(self):
        resp = requests.get(
            url='https://player.stv.tv/categories/dramas',
        )
        self.assertEqual(resp.status_code, 200)
        html = resp.text

        result = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html,
                           flags=re.DOTALL)
        json_str = result[1]
        data = json.loads(json_str)
        programmes = data['props']['pageProps']['data']['assets']
        for pgm in programmes:
            self.check_programme(pgm)