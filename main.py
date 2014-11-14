#coding=utf-8
__author__ = 'popka'

from Page import Page
from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from Utils import utils
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
from LinkContainer import LinkContainer
import time


urls_with_parameters = []
browser = 'CHROME'
MAX_PAGES = 30

def add_link(url, driver): """
Функция примиет на вход url, находит на странице все ссылки в пределах
этого сайта и добавляет их в links. Не должно быть повторений
:param url:
:param driver:
:return:
"""
pass


if __name__ == '__main__':

    MAIN_URL = "http://yandex.ru/" # Считывать, как аргумент командной строки, обязательно / в конце!

    driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
    )

    link_container = LinkContainer()
    link_container.add([MAIN_URL])

    i = 0
    while ((i < link_container.get_length()) and (i < MAX_PAGES)):
        url = link_container.get_link(i)
        print(i, url)
        page = Page(driver=driver, url=url)
        urls_with_parameters += page.try_page() # Подумать об уникальности урлов с параметрами
        link_container.add(page.get_inner_links())

        i += 1
        time.sleep(0.5)

    print(urls_with_parameters)

    driver.quit()