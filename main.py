#coding=utf-8
import argparse

__author__ = 'popka'

from PageClass.Page import Page
from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from Utils import utils
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
import LinkContainer
from Utils.utils import ajax_complete
import time
import os
from XssChecker import XssChecker

browser = 'FIREFOX'
MAX_PAGES = 60
QUEST_SYMBOL_SUPPORTED = False
MAIN_URL = ""

'''
Заметка
Добавить проверку на jQuery. wait_for_ajax не сработает без него!
'''

def try_one_page(driver, url):
    pageo = Page(driver=driver, url=url)
    pageo.open()
    return pageo.try_page()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login', action='store_const', const=True, default=False)
    parser.add_argument('url')
    parser.add_argument('-o', '--one', action='store_const', const=True, default=False)
    return parser

if __name__ == '__main__':

    """
    Чтобы не включать selenuim сервер руками. Через раз работает. ХЗ почему.
    os.system("command")
    os.system('java -jar Selenium/selenium-server-standalone-2.43.1.jar')
    time.sleep(2)
    """

    parser = create_parser()
    namespace = parser.parse_args()

    MAIN_URL = namespace.url # Считывать, как аргумент командной строки

    driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
    )

    # auth ВВОД ВРЕМЕНИ, Отводимого на авторизацию
    if namespace.login:
        page = Page(driver=driver, url=MAIN_URL)
        page.open()
        time.sleep(20)

    if namespace.one is False:
        #'''
        #КАРТА САЙТА. Нужна, если чекаем все урлы на страничке (обычный случай)

        link_container = LinkContainer.LinkContainer()
        link_container.add([MAIN_URL])

        urls_with_parameters = []
        i = 0
        print('Generating map of site')

        while ((i < link_container.get_length()) and (i < MAX_PAGES)):
            url = link_container.get_link(i)
            print('.')

            page = Page(driver=driver, url=url)
            page.open()

            link_container.add(page.get_inner_links())

            urls_with_parameters += page.try_page()

            i += 1
            time.sleep(0.5)

        urls_with_parameters = set(urls_with_parameters) #Сделать список уникальным

        print(link_container.get_all_links())
        print(urls_with_parameters)

        #''' Карта сайта

        urls_with_parameters = set()
    else:
        # ЕСЛИ ОДИН УРЛ ВКЛЮЧАЕМ ЭТО ВЕТВЛЕНИЕ ВМЕСТО ВЕРХНЕГО
        urls_with_parameters = set(try_one_page(driver=driver, url=MAIN_URL))

    print(urls_with_parameters)
    xss_checker = XssChecker(driver)

    #Если обычный поиск
    print('Finding xss...')
    for url in urls_with_parameters:
        xss_checker.find_xss(url)

    print("RESULT:")
    print(xss_checker.xss_urls)

    # Если поиск в диалоге, может глючить. Для него не нужна карта сайта!
    #xss_checker.find_xss_in_one_page(MAIN_URL)

    driver.quit()
