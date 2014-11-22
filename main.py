#coding=utf-8
__author__ = 'popka'

from Page import Page
from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from Utils import utils
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
import LinkContainer
import time
import os
from XssChecker import XssChecker
os.system("command")

browser = 'CHROME'
MAX_PAGES = 60
QUEST_SYMBOL_SUPPORTED = False
MAIN_URL = ""

'''
Заметка
Добавить проверку на jQuery. wait_for_ajax не сработает без него!
'''


if __name__ == '__main__':

    #os.system('java -jar Selenium/selenium-server-standalone-2.43.1.jar')
    #time.sleep(2)

    MAIN_URL = "http://www.insecurelabs.org/Task/" # Считывать, как аргумент командной строки, обязательно '/' в конце!

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

        if page.is_alert_appear():
            print('text = ', page.get_alert_text_and_close())

        i += 1
        time.sleep(0.5)

    urls_with_parameters = set(urls_with_parameters) #Сделать список уникальным

    print(link_container.get_all_links())
    print(urls_with_parameters)

    #xss_checker = XssChecker(driver)
    #for url in urls_with_parameters:
     #   xss_checker.find_xss(url)

    driver.quit()
