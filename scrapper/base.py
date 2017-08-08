from selenium import webdriver


class BaseScrapper:

    SLEEP_TIME = 3

    # Base on Iphone 6
    MOBILE_WIDTH = 375
    MOBILE_HEIGTH = 667

    def __init__(self, website_url):
        self.website_url = website_url
        self.browser = self._open_mobile_browser()

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
        self.browser.implicitly_wait(sleep_time)

    def resize_window(self, width, heigth):
        self.browser.set_window_size(width, heigth)

    def to_mobile_dimension(self):
        self.resize_window(self.MOBILE_WIDTH, self.MOBILE_HEIGTH)


class InstaScrapper(BaseScrapper):

    def login(self, username, password):
        # self.browser.find_element_by_class_name('_fcn8k').click()
        self.browser.find_element_by_xpath("//article/div/div/p/a[text()='Log in']").click()
        self.wait(2)

        username_input = self.browser.find_element_by_xpath("//input[@name='username']")
        password_input = self.browser.find_element_by_xpath("//input[@name='password']")

        username_input.send_keys(username)
        password_input.send_keys(password)

        self.browser.implicitly_wait(self.SLEEP_TIME)
        self.browser.find_element_by_xpath("//form/span/button[text()='Log in']").click()

        print('Welkome... in DUTCH {0}'.format(username))

        self.wait(5)

    def logout(self):
        self._close_browser()

    def upload_picture(self, image_path):
        print('uploading picture...', image_path)

        # simulate the click in the Camera Logo
        image_input = self.browser.find_element_by_class_name('coreSpriteCameraInactive').click()
        self.wait(5)

        image_input = self.browser.find_element_by_class_name('_loq3v')
        image_input.send_keys(image_path)
        self.wait(4)
