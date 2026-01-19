from unittest import TestCase

from codequick import Listitem

from resources.lib.channels.uk import watchfreeuk


class MainMenu(TestCase):
    def test_main_menu(self):
        li_items = watchfreeuk.main_menu.test()
        self.assertEqual(len(li_items), 5)


class ListRenderable(TestCase):
    def test_list_slider(self):
        url = ("https://www.watchfreeuk.co.uk/renderable/slider/rendered?endpoint=%2Fapi%2Fpage%2Fhome&path=sections.7.tiles&finder=%5B%5D&slider=%7B%22id%22%3A%22playlist%5C%2F5317%22%2C%22title%"
               "22%3A%22Vintage+Vault%22%2C%22showTitle%22%3Atrue%2C%22showPlay%22%3Afalse%2C%22showAll%22%3Anull%2C%22image_type%22%3A%2216%3A9%22%2C%22displayType%22%3A%22large_row%22%2C%22type%"
               "22%3A%22SHOW_ALL%22%2C%22npaw_path%22%3A%22Home%3EVintage+Vault+8%5C%2F10%22%2C%22entitlements%22%3A%5B%22Free%22%2C%22simplestream-vip%22%5D%2C%22cache%22%3A%7B%22key%22%3A%22comp"
               "any_136_page_21_section_1084_cc_gb_lang_en_platform_web_region_id_300.json%22%2C%22type%22%3A%22database%22%2C%22minutes%22%3A60%2C%22created_at%22%3A%222025-10-01+21%3A30%3A17%22%"
               "2C%22expires_at%22%3A%222025-10-01+22%3A30%3A17%22%7D%2C%22hasLogo%22%3Atrue%7D&cc=GB")
        li_items = watchfreeuk.list_renderable_component.test(url)
        self.assertGreater(len(li_items), 5)
        for item in li_items:
            self.assertIsInstance(item, Listitem)


class ListPage(TestCase):
    def test_list_Home(self):
        li_items = watchfreeuk.list_home_page.test('https://www.watchfreeuk.co.uk/')
        self.assertGreater(len(li_items), 5)

    def test_list_true_crime(self):
        li_items = watchfreeuk.list_page.test('https://www.watchfreeuk.co.uk/page/true-crime')
        self.assertGreater(len(li_items), 5)

    def test_list_legend(self):
        li_items = watchfreeuk.list_page.test('https://www.watchfreeuk.co.uk/page/legend')
        self.assertGreater(len(li_items), 5)


class ListSeriesAndEpisodes(TestCase):
    show_url = 'https://www.watchfreeuk.co.uk/shows/9f32008b-01b5-11eb-8876-0aa1bd83af14/psychic-private-eyes'

    def test_list_series(self):
        li_items = watchfreeuk.list_series.test(self.show_url)
        self.assertGreater(len(li_items), 1)

    def test_list_episodes(self):
        li_items = list(watchfreeuk.list_episodes.test(self.show_url, 'season-1'))
        self.assertGreater(len(li_items), 5)


