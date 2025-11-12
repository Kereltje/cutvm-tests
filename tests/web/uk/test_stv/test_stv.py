import requests

from unittest import TestCase

from credentials import credentials

from resources.lib.channels.uk import stv

class StvCategories(TestCase):
    def test_get_categories(self):
        cats = stv.list_categories.test(None)
        self.assertEqual(len(cats), 29)


class StvProgrammes(TestCase):
    def test_get_categorie_entertainment(self):
        pgms_list = stv.list_programs.test(None, 'entertainment')
        self.assertGreater(len(pgms_list), 75)