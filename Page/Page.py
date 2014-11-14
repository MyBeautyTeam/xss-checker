#coding=utf-8
__author__ = 'popka'

import urlparse
import Utils.utils as utils
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException, WebDriverException


class Page(object):
    PATH = ''
    BUTTON = "button"
    INPUT_SUBMIT = 'input[type=submit]'
    INPUT_IMAGE = 'input[type=image]'
    LINKS = 'a'

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        url = urlparse.urljoin(self.url, self.PATH)
        self.driver.get(url)
        utils.wait_for_document_ready(self.driver)

    def _fill_all_input(self):
        '''
        Заполняет все input на странице текстом
        '''
        self.driver.execute_script(utils.fill_all_input)

    def _get_all_button(self):
        '''
        возвращает массив всех "кнопок"
        :return:
        '''
        button = self.driver.find_elements_by_tag_name(self.BUTTON)
        button += (self.driver.find_elements_by_css_selector(self.INPUT_SUBMIT))
        button += (self.driver.find_elements_by_css_selector(self.INPUT_IMAGE))
        return button

    def get_inner_links(self):
        '''
        Возвращает массив ссылок, находящихся, находящихся внутри домена
        :return:
        '''
        all_links = self.driver.find_elements_by_tag_name(self.LINKS)

        #Доменное имя
        domain = self.url[self.url.index("://")+3:]
        domain = domain[:domain.index("/")]

        inside_links = []

        for link in all_links:
            href = link.get_attribute('href')

            if href is not None:
                if (domain in href): # По настройке можно выключить поддержку поддоменов '.'+domain not in href. но нужна еще проверка на www
                    inside_links.append(href)

#                    print(href)

        return inside_links


    def try_page(self):
        """
            Для каждой кнопки заполняем все input и нажимаем на нее.
            Если в результате нажатия срабатывает ajax(пока нету),
            или нас редиректит на ссылку с параметрами (содержит '?'),
            то записываем ее в список интересных ссылок

            возвращает список интересных ссылок
        """
        self.open()

        urls_with_parameters = []

        buttons = self._get_all_button()
        buttons_count = len(buttons) # Определяем количество подходящих нам кнопок

        for i in xrange(buttons_count):
            self.open()
            buttons = self._get_all_button()

            try:
                self._fill_all_input()
                buttons[i].click()

                utils.wait_for_ajax_complete(self.driver)
                utils.wait_for_document_ready(self.driver) # Достаточно прогрузки шапки, поменять

                if '?' in self.driver.current_url:
                    urls_with_parameters.append(self.driver.current_url)

            except (StaleElementReferenceException, ElementNotVisibleException, WebDriverException):
                pass

        return urls_with_parameters









