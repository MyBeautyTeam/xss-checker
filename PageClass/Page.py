#coding=utf-8
__author__ = 'popka'

import urlparse
import Utils.utils as utils
from selenium.common.exceptions import WebDriverException, TimeoutException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import re
import urllib



class Page(object):
    PATH = ''
    FORM = "form"
    LINKS = 'a'

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        url = urlparse.urljoin(self.url, self.PATH)
        self.driver.get(url)
        utils.wait_for_document_ready(self.driver)

    def open_without_wait(self):
        url = urlparse.urljoin(self.url, self.PATH)
        self.driver.get(url)
        #utils.wait_for_document_ready(self.driver)

    def _fill_all_input(self):
        '''
        Заполняет все input на странице текстом
        '''
        self.driver.execute_script(utils.fill_all_input)

    def _get_all_forms(self):
        '''
        возвращает массив всех форм
        :return:
        '''
        button = self.driver.find_elements_by_tag_name(self.FORM)
        return button

    def get_inner_links(self):
        '''
        Возвращает массив ссылок, находящихся, находящихся внутри домена
        :return:
        '''
        all_links = self.driver.find_elements_by_tag_name(self.LINKS)

        domain = self.url[self.url.index("://")+3:] #Доменное имя
        domain = domain[:domain.index("/")]

        regular = re.compile('\.+\w+$', re.IGNORECASE) #Поиск конструкций вида .doc

        inside_links = []

        for link in all_links:
            href = link.get_attribute('href')

            if href is not None:
                if (domain in href): # Находимся ли мы в пределах сайта?
                    # По настройке можно выключить поддержку поддоменов '.'+domain not in href. но нужна еще проверка на www

                    if '#' in href: #Если есть '#' - отрезаем ее
                        href = href[0:href.index('#')]

                    href_without_domain = href[href.index(domain)+len(domain):] # выделяем часть урла без доменного имени
                    extensions = regular.findall(href_without_domain) # производим по нему поиск конструкций типа .doc

                    if len(extensions) == 0: #Если нет конструции вида .doc,
                        inside_links.append(href)
                    else:
                        extensions = extensions[0]
                        if extensions=='.html' or extensions=='.htm' or extensions == '.xml': #Продолжать список согласно опыту
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

        forms = self._get_all_forms()
        forms_count = len(forms) # Определяем количество подходящих нам кнопок

        for i in xrange(forms_count):
            self.open()
            forms = self._get_all_forms()
            try:
                self._fill_all_input()
                forms[i].submit()

                utils.wait_for_ajax_complete(self.driver)
                utils.wait_for_head_load(self.driver) # Достаточно прогрузки шапки, поменять

                if '?' in self.driver.current_url:

                    decoded_url = urllib.unquote(self.driver.current_url).decode('utf8')
                    urls_with_parameters.append(decoded_url)

            except (StaleElementReferenceException, ElementNotVisibleException, WebDriverException):
                pass

        return urls_with_parameters

    def is_alert_appear(self):
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.alert_is_present())
            return True

        except TimeoutException:
            return False

    def get_alert_text_and_close(self):

        alert = self.driver.switch_to_alert()
        text = alert.text
        alert.accept()

        return text


    def find_element_by_tag_and_attributes(self, tag, attr):
        elements = self.driver.find_elements_by_tag_name(tag)
        for el in elements:
            count_of_hit_attribute = 0
            for attribute in attr:
                attrib = el.get_attribute(attribute)
                attr_attr = attr[attribute]
                if (el.get_attribute(attribute) is not None):
                    if (attr[attribute] in el.get_attribute(attribute)):
                        count_of_hit_attribute += 1

            if (count_of_hit_attribute == len(attr)):
                return True

        return False









