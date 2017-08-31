import logging
import time
import random
from selenium import webdriver
from pyvirtualdisplay import Display
from pyinstamation.scrapper.instagram_const import DRIVER_LOCATION
from pyinstamation.scrapper.utils import save_page_source
from pyinstamation import CONFIG


logger = logging.getLogger(__name__)


class BaseScrapper:

    # Base on Iphone 6
    MOBILE_WIDTH = 375
    MOBILE_HEIGTH = 667

    def __init__(self, website_url='https://www.instagram.com', hide_browser=False):
        self.website_url = website_url
        self.browser = None
        self.hide_browser = CONFIG.get('hide_browser', hide_browser)

    def open_browser(self):
        if self.hide_browser:
            self.display = Display(visible=0, size=(self.MOBILE_WIDTH, self.MOBILE_HEIGTH))
            self.display.start()
        self.browser = self._open_mobile_browser()

    def _open_mobile_browser(self):
        mobile_emulation = {"deviceName": "Nexus 5"}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_prefs = {
            'intl.accept_languages': 'en-US'
        }
        chrome_options.add_experimental_option('prefs', chrome_prefs)
        return webdriver.Chrome(
            DRIVER_LOCATION,
            desired_capabilities=chrome_options.to_capabilities())

    def close_browser(self):
        logger.debug('Closing browser...')
        self.browser.close()
        if self.hide_browser:
            self.display.stop()
        self.browser = None

    def find(self, method, selector, wait=True, explicit=True, sleep_time=None, **kwargs):
        if wait:
            self.wait(sleep_time=sleep_time, explicit=explicit)

        _find = getattr(self.browser, 'find_element_by_%s' % method)
        return _find(selector, **kwargs)

    @property
    def page_source(self):
        return self.browser.page_source

    def get_page(self, url, sleep_time=3):
        self.browser.get(url)
        self.wait(sleep_time=sleep_time, explicit=True)
        save_page_source(url, self.page_source)

    def wait(self, sleep_time=None, explicit=False):
        """
        Implicit wait
        """
        if sleep_time is None:
            sleep_time = self.random_seconds()
        if explicit:
            time.sleep(sleep_time)
        else:
            self.browser.implicitly_wait(sleep_time)
        return sleep_time

    @staticmethod
    def random_seconds():
        return random.randrange(1, 10)

    def resize_window(self, width, heigth):
        self.browser.set_window_size(width, heigth)

    def to_mobile_dimension(self):
        self.resize_window(self.MOBILE_WIDTH, self.MOBILE_HEIGTH)
