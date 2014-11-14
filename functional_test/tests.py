import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return

        super(NewVisitorTest, cls).setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(NewVisitorTest, cls).tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_see_title_and_header(self):
        # Tesla goes to check out the home page
        self.browser.get(self.server_url)

        # He notices the title mentions ShowCase
        self.assertIn('ShowCase', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('ShowCase', header_text)

    def test_layout_and_styling(self):
        # Tesla goes to home page.
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        jumbotron = self.browser.find_element_by_class_name("jumbotron")
        self.assertAlmostEqual(jumbotron.location['x'] + jumbotron.size['width'] / 2, 512, delta=5)
