__author__ = 'popka'

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


fill_all_input = 'var inputs = document.querySelectorAll("input"); ' \
                 'for (var i=0; i<inputs.length; i++) {' \
                    'inputs[i].value = "abcd"' \
                 '}'


def is_document_ready(driver):
    try:
        return "complete" == driver.execute_script("return document.readyState")
    except WebDriverException:
        pass


def wait_for_document_ready(driver):
    try:
        WebDriverWait(driver, 10, 1).until(is_document_ready, 'document ready')
    except TimeoutException:
        pass


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass


def wait_for_ajax_complete(driver):
    try:
        WebDriverWait(driver, 10, 3).until(ajax_complete, 'AJAX')
    except TimeoutException:
        pass