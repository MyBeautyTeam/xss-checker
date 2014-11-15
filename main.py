#coding=utf-8
__author__ = 'popka'

from Page import Page
from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from Utils import utils
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
import LinkContainer
import time


browser = 'CHROME'
MAX_PAGES = 60
QUEST_SYMBOL_SUPPORTED = False

def add_link(url, driver): """
Функция примиет на вход url, находит на странице все ссылки в пределах
этого сайта и добавляет их в links. Не должно быть повторений
:param url:
:param driver:
:return:
"""
pass


if __name__ == '__main__':

    MAIN_URL = "http://vk.com/" # Считывать, как аргумент командной строки, обязательно '/' в конце!

    driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
    )

    link_container = LinkContainer.LinkContainer()
    link_container.add([MAIN_URL])

    urls_with_parameters = []
    i = 0

    while ((i < link_container.get_length()) and (i < MAX_PAGES)):
        url = link_container.get_link(i)
        print(i, url, link_container.get_length())
        page = Page(driver=driver, url=url)
        page.open()
        link_container.add(page.get_inner_links())

        urls_with_parameters += page.try_page()

        i += 1
        time.sleep(0.5)

    urls_with_parameters = set(urls_with_parameters) #Сделать список уникальным

    print(link_container.get_all_links())
    print(urls_with_parameters)

    driver.quit()