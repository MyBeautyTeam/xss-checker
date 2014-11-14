__author__ = 'popka'

import urlparse
import Utils.utils as utils


class Page(object):
    PATH = ''
    BUTTON = "button"
    INPUT_SUBMIT = 'input[type=submit]'
    INPUT_IMAGE = 'input[type=image]'

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        url = urlparse.urljoin(self.url, self.PATH)
        self.driver.get(url)
        utils.wait_for_document_ready(self.driver)

    def fill_all_input(self):
        self.driver.execute_script(utils.fill_all_input)

    def get_all_button(self):
        button = self.driver.find_elements_by_tag_name(self.BUTTON)
        button += (self.driver.find_elements_by_css_selector(self.INPUT_SUBMIT))
        button += (self.driver.find_elements_by_css_selector(self.INPUT_IMAGE))
        return button




