import time

from selenium import webdriver


class BaseScrapper:

    SLEEP_TIME = 3

    # Base on Iphone 6
    MOBILE_WIDTH = 375
    MOBILE_HEIGTH = 667

    def __init__(self, website_url):
        self.website_url = website_url
        self.browser = self._open_mobile_browser()

    def _open_browser(self):
        return webdriver.Chrome()

    def _open_mobile_browser(self):
        mobile_emulation = {"deviceName": "Nexus 5"}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        return webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities())

    def _close_browser(self):
        self.browser.close()

    def reach_website(self):
        self.browser.get(self.website_url)
        self.wait(3)

    def wait(self, sleep_time=SLEEP_TIME):
        """
        Implicit wait
        """
        self.browser.implicitly_wait(sleep_time)

    @staticmethod
    def wait_explicit(seconds=3):
        time.sleep(seconds)

    def resize_window(self, width, heigth):
        self.browser.set_window_size(width, heigth)

    def to_mobile_dimension(self):
        self.resize_window(self.MOBILE_WIDTH, self.MOBILE_HEIGTH)
