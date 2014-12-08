#coding=utf-8
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


if __name__ == '__main__':

    #os.system("command")
    #os.system('java -jar Selenium/selenium-server-standalone-2.43.1.jar')
    #time.sleep(2)

    #MAIN_URL = "https://xss-doc.appspot.com/demo/2" # Считывать, как аргумент командной строки, обязательно '/' в конце!
    MAIN_URL = "http://192.168.5.52/DVWA-1.0.8/" # Считывать, как аргумент командной строки


    driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
    )

    # ======= auth
    page = Page(driver=driver, url=MAIN_URL)
    page.open()
    time.sleep(20)
    # =======

    '''
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

    '''

    #urls_with_parameters = set(['https://xss-doc.appspot.com/demo/2?query=abcd']) #Сделать список уникальным

    urls_with_parameters = set()

    if (True): # ЕСЛИ ОДИН УРЛ ВКЛЮЧАЕМ ЭТУ ФУНКЦИЮ
        urls_with_parameters = set(try_one_page(driver=driver, url='http://192.168.5.52/DVWA-1.0.8/vulnerabilities/xss_r/'))

    print(urls_with_parameters)
    #urls_with_parameters = set(['http://192.168.5.52/DVWA-1.0.8/vulnerabilities/xss_r/?name=abcd#']) #Сделать список уникальным
    xss_checker = XssChecker(driver)
    print('Finding xss...')
    for url in urls_with_parameters:
        xss_checker.find_xss(url)

    #driver.quit()
