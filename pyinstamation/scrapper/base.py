import logging
import time
import random
from urllib.parse import urlparse
from selenium import webdriver
from pyvirtualdisplay import Display
# from pyinstamation.scrapper.instagram_const import DRIVER_LOCATION, HOSTNAME
from pyinstamation.scrapper import instagram_const as const
from pyinstamation.scrapper.utils import save_page_source
from pyinstamation import CONFIG
from urllib.parse import urljoin


logger = logging.getLogger(__name__)


class BaseScrapper:

    # Base on Iphone 6
    MOBILE_WIDTH = 375
    MOBILE_HEIGTH = 667

    def __init__(self, hide_browser=False):
        self.browser = None
        self.display = None
        self.hide_browser = CONFIG.get('hide_browser', hide_browser)
        self.pagination_info = {}

    @staticmethod
    def random_seconds():
        return random.randrange(1, 5)

    def open_browser(self):
        # if self.hide_browser:
        size = (self.MOBILE_WIDTH + 1, self.MOBILE_HEIGTH + 1)
        self.display = Display(visible=int(not self.hide_browser), size=size)
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
            const.DRIVER_LOCATION,
            desired_capabilities=chrome_options.to_capabilities())

    def close_browser(self):
        logger.debug('Closing browser...')
        if self.browser is not None:
            self.browser.quit()
            self.browser = None
        if self.display is not None:
            self.display.stop()

    def find(self, method, selector, wait=True, explicit=True,
             sleep_time=None, **kwargs):
        if wait:
            self.wait(sleep_time=sleep_time, explicit=explicit)

        _find = getattr(self.browser, 'find_element_by_%s' % method)
        return _find(selector, **kwargs)

    @property
    def page_source(self):
        return self.browser.page_source

    @property
    def current_url(self):
        return urlparse(self.browser.current_url)

    def get_page(self, path, sleep_time=None):
        _url = urljoin(const.HOSTNAME, path)

        if sleep_time is None:
            sleep_time = self.random_seconds()

        if self.current_url == urlparse(_url):
            # use already loaded page
            save_page_source(path, self.page_source)
            return False

        self.browser.get(_url)
        self.wait(sleep_time=sleep_time, explicit=True)
        save_page_source(path, self.page_source)
        return True

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

    def resize_window(self, width, heigth):
        self.browser.set_window_size(width, heigth)

    def to_mobile_dimension(self):
        self.resize_window(self.MOBILE_WIDTH, self.MOBILE_HEIGTH)

    @staticmethod
    def get_network_script():
        script = "var performance = window.performance || window.mozPerformance ||" \
                 "window.msPerformance || window.webkitPerformance || {};" \
                 "var network = performance.getEntries() || {}; return network;"

        return script

    def get_network_activity(self):
        return self.browser.execute_script(self.get_network_script())
