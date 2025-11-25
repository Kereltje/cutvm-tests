from unittest import TestCase

from codequick import Listitem

from resources.lib.channels.uk import uktvplay



class HomePage(TestCase):
    def test_collections(self):
        li_items = uktvplay.list_collections.test()