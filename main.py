#coding=utf-8
__author__ = 'popka'

from Page import Page
from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from Utils import utils
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException


links = []
urls_with_parameters = []
browser = 'CHROME'

def try_page(url, driver):

    page = Page(driver, url)
    page.open()

    buttons = page.get_all_button()
    buttons_count = len(buttons) # Определяем количество подходящих нам кнопок

    for i in xrange(buttons_count):
        """
        Для каждой кнопки заполняем все input и нажимаем на нее.
        Если в результате нажатия срабатывает ajax(пока нету),
        или нас редиректит на ссылку с параметрами (содержит '?'),
        то записываем ее в список интересных ссылок
        """
        page.open()
        buttons = page.get_all_button()
        try:
            page.fill_all_input()
            buttons[i].click()

            utils.wait_for_ajax_complete(driver)
            utils.wait_for_document_ready(driver) # Достаточно прогрузки шапки, поменять

            if '?' in driver.current_url:
                urls_with_parameters.append(driver.current_url)

        except (StaleElementReferenceException, ElementNotVisibleException):
            pass

    print(urls_with_parameters)


def add_link(url, driver): """
Функция примиет на вход url, находит на странице все ссылки в пределах
этого сайта и добавляет их в links. Не должно быть повторений
:param url:
:param driver:
:return:
"""
pass


if __name__ == '__main__':

    links.append("https://mail.ru/")

    driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
    )

    for url in links:
        add_link()
        try_page(url, driver)

    driver.quit()