
import requests

from unittest import TestCase


class HomePage(TestCase):
    def test_get_homepage(self):
        resp = requests.get(
            url='https://xroad.uktvapi.co.uk/build/',
            params={
                'anon_id': '6e1608cc-ad28-4be8-bce0-5cad81b886e4',
                'page': 'home',
                'platform_name': 'uktvplay',
                'platform_type': 'web',
                'preprocess': '1',
                'version': '2',
                'partprocess_from':'1',
                'partprocess_to': '24'}
        )
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertIsInstance(data, dict)