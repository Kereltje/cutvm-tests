
import os

from codequick import Listitem
from htmlement import HTMLement
from xml.etree import ElementTree

from unittest import TestCase
from unittest.mock import patch

from resources.lib.channels.uk import watchfreeuk

from testutils import open_doc


my_dir = os.path.abspath(os.path.dirname(__file__))


def parse_html(text):
    parser = HTMLement()
    parser.feed(text)
    return parser.close()


class TestUtiles(TestCase):
    def test_get_all_text(self):
        div = ElementTree.fromstring("""
        <div><span class="mycls">
            1
            <span>
                2
                3
                <span>4</span>
            </span>
            </span></div>""")
        text = watchfreeuk.get_all_texts(div)
        self.assertEqual("1 2 3 4", text)

        span = ElementTree.fromstring("""
                <span class="mycls">
                    1
                    <span>
                        2
                        3
                        <span>4</span>
                    </span>
                    </span>""")
        text = watchfreeuk.get_all_texts(span)
        self.assertEqual("1 2 3 4", text)


class HomePage(TestCase):
    def test_hero_params_from_x_data(self):
        hero_data = """
        enderableComponent({
                    show: false,
                    url: {
                        params: {},
                        paramString: ''
                    },
                    buildParams() {
                        this.url.params = {
                            endpoint: '\/api\/page\/home',
                            path: 'sections.0.tiles',
                            cc: 'GB',
                            fromHome: true            }


                        this.url.paramString = new URLSearchParams(this.url.params);
                        this.url.paramString = this.url.paramString.toString();
                    },
                })
        """
        params = watchfreeuk.params_from_x_data(hero_data)
        self.assertEqual(len(params), 4)
        for k in ('endpoint', 'path', 'cc', 'fromHome'):
            self.assertTrue(k in params)

    def test_slider_params_from_x_data(self):
        slider_data = """
        RenderableComponent({
                show: false,
                slider: null,
                url: {
                    params: {},
                    paramString: ''
                },
                buildParams() {
                    this.url.params = {
                        endpoint: '/api/page/home',
                        path: 'sections.1.tiles',
                        finder: '[]',
                        slider: '{\u0022id\u0022:\u0022playlist\\\/5406\u0022,\u0022title\u0022:\u0022Just in..\u0022,\u0022showTitle\u0022:true,\u0022showPlay\u0022:false,\u0022showAll\u0022:\u0022playlist\\\/5406\u0022,\u0022image_type\u0022:\u002216:9\u0022,\u0022displayType\u0022:\u0022large_row\u0022,\u0022type\u0022:\u0022SHOW_ALL\u0022,\u0022npaw_path\u0022:\u0022Home\u003EJust in.. 2\\\/10\u0022,\u0022entitlements\u0022:[\u0022Free\u0022,\u0022simplestream-vip\u0022],\u0022cache\u0022:{\u0022key\u0022:\u0022company_136_page_21_section_947_cc_gb_lang_en_platform_web_region_id_300.json\u0022,\u0022type\u0022:\u0022cache\u0022,\u0022minutes\u0022:60,\u0022created_at\u0022:\u00222025-09-26 02:01:20\u0022,\u0022expires_at\u0022:\u00222025-09-26 03:01:20\u0022},\u0022hasLogo\u0022:true}',
                        cc: 'GB'            }


                    this.url.paramString = new URLSearchParams(this.url.params);
                    this.url.paramString = this.url.paramString.toString();
                },
            })
        """
        params = watchfreeuk.params_from_x_data(slider_data)
        self.assertEqual(len(params), 5)
        for k in ('endpoint', 'path', 'finder', 'slider', 'cc'):
            self.assertTrue(k in params)

    def test_hero_path_from_x_data(self):
        hero_data = """
        this.element = $el;buildParams();if(!rendered && !rendering) {await render(
        '/renderable/sliderhero/rendered?' + url.paramString);}"""
        path = watchfreeuk.path_from_x_data(hero_data)
        self.assertEqual(path, '/renderable/sliderhero/rendered?')

    def test_slider_path_from_x_data(self):
        slider_data = """
        if(!rendered && !rendering) {
                    await render(
                        '/renderable/slider/rendered?' + url.paramString
                    );
                }
        """
        path = watchfreeuk.path_from_x_data(slider_data)
        self.assertEqual(path, '/renderable/slider/rendered?')

    def test_slider_renderable_url(self):
        div_obj = ElementTree.fromstring(r"""
        <div class="position-relative z-1 z-2-hover"
             x-data="RenderableComponent({
                show: false,
                slider: null,
                url: {
                    params: {},
                    paramString: ''
                },
                buildParams() {
                    this.url.params = {
                        endpoint: '/api/page/home',
                        path: 'sections.3.tiles',
                        finder: '[]',
                        slider: '{\u0022id\u0022:\u0022playlist\\\/6171\u0022,\u0022title\u0022:\u0022British Crime Movies\u0022,\u0022showTitle\u0022:true,\u0022showPlay\u0022:false,\u0022showAll\u0022:null,\u0022image_type\u0022:\u002216:9\u0022,\u0022displayType\u0022:\u0022large_row\u0022,\u0022type\u0022:\u0022SHOW_ALL\u0022,\u0022npaw_path\u0022:\u0022Home\u003EBritish Crime Movies 4\\\/10\u0022,\u0022entitlements\u0022:[\u0022Free\u0022,\u0022simplestream-vip\u0022],\u0022cache\u0022:{\u0022key\u0022:\u0022company_136_page_21_section_3271_cc_gb_lang_en_platform_web_region_id_300.json\u0022,\u0022type\u0022:\u0022cache\u0022,\u0022minutes\u0022:60,\u0022created_at\u0022:\u00222025-09-26 02:01:21\u0022,\u0022expires_at\u0022:\u00222025-09-26 03:01:21\u0022},\u0022hasLogo\u0022:true}',
                        cc: 'GB'            }


                    this.url.paramString = new URLSearchParams(this.url.params);
                    this.url.paramString = this.url.paramString.toString();
                },
            })"
                        x-init="this.element = $el; buildParams();"
                        x-intersect="
                if(!rendered &amp;&amp; !rendering) {
                    await render(
                        '/renderable/slider/rendered?' + url.paramString
                    );
                }
            "
        ></div>
        """)
        url = watchfreeuk.renderable_url(div_obj)
        self.assertTrue(url.startswith('https://www.watchfreeuk.co.uk/renderable/slider/rendered?'))
        self.assertTrue('%22hasLogo%22' in url)

    def test_hero_renderable_url(self):
        div_obj = ElementTree.fromstring(r"""
        <div class="position-relative"
                        x-data="RenderableComponent({
                            show: false,
                            url: {
                                params: {},
                                paramString: ''
                            },
                            buildParams() {
                                this.url.params = {
                                    endpoint: '\/api\/page\/home',
                                    path: 'sections.0.tiles',
                                    cc: 'GB',
                                    fromHome: true            }


                                this.url.paramString = new URLSearchParams(this.url.params);
                                this.url.paramString = this.url.paramString.toString();
                            },
                        })"
                        x-init="this.element = $el;buildParams();if(!rendered &amp;&amp; !rendering) {await render('/renderable/sliderhero/rendered?' + url.paramString);}"
                ></div>
                """)
        url = watchfreeuk.renderable_url(div_obj)
        self.assertTrue(url.startswith('https://www.watchfreeuk.co.uk/renderable/sliderhero/rendered?'))
        self.assertTrue('fromHome=true' in url)

    @patch("resources.lib.channels.uk.watchfreeuk.fetch",
           return_value=parse_html(open_doc('home.html', my_dir)))
    def test_home_page(self, _):
        li_items = watchfreeuk.list_home_page.test('home')
        self.assertEqual(10, len(li_items))
        for li in li_items[1:]:
            self.assertIsInstance(li, Listitem)


class RenderableComponent(TestCase):
    def test_slider2(self):
        for slider_doc in ('slider1.html', 'slider2.html', 'slider3.html', 'slider4.html', 'slider6.html', 'slider7.html'):
            with patch("resources.lib.channels.uk.watchfreeuk.fetch",
                       return_value=parse_html(open_doc(slider_doc, my_dir))):
                li_items = watchfreeuk.list_renderable_component.test("renderabel_url")
                self.assertGreater(len(li_items), 5)
                for item in li_items:
                    self.assertIsInstance(item, Listitem)

    @patch("resources.lib.channels.uk.watchfreeuk.fetch",
           return_value=parse_html(open_doc('renderable_search_result.html', my_dir)))
    def test_search_result(self, _):
        li_items = watchfreeuk.list_renderable_component.test("search-result")
        self.assertGreater(len(li_items), 5)
        for item in li_items:
            self.assertIsInstance(item, Listitem)


class ListPage(TestCase):
    @patch("resources.lib.channels.uk.watchfreeuk.fetch",
           return_value=parse_html(open_doc('playlist_legend.html', my_dir)))
    def test_list_playlist_legend_page(self, _):
        """The page of collection 'LEGEND' has a different structure; it contains
        only a single slider and must be parsed like a normal slider's renderable
        content.

        """
        with patch('resources.lib.channels.uk.watchfreeuk.list_renderable_component') as mocked_list_renderable:
            li_items = watchfreeuk.list_page.test(url='legend.html', fallback_url='legend_slider.html')
        mocked_list_renderable.assert_called_once()
        self.assertEqual(mocked_list_renderable.call_args.args[1], 'legend_slider.html')


@patch("resources.lib.channels.uk.watchfreeuk.fetch",
        return_value=parse_html(open_doc('series_page.html', my_dir)))
class ListSeriesAndEpisodes(TestCase):
    def test_list_series(self, _):
        li_items = watchfreeuk.list_series.test('series page')
        self.assertEqual(2, len(li_items))
        for item in li_items:
            self.assertIsInstance(item, Listitem)

    def test_list_episodes(self, _):
        li_items = watchfreeuk.list_episodes.test(url='series page', series='season-1')
        self.assertEqual(10, len(li_items))
        for item in li_items:
            self.assertIsInstance(item, Listitem)

        li_items = watchfreeuk.list_episodes.test(url='series page', series='season-2')
        self.assertEqual(9, len(li_items))
        for item in li_items:
            self.assertIsInstance(item, Listitem)