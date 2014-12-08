__author__ = 'popka'

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait



def get_fill_all_input_script(text):
    script = 'var inputs = document.querySelectorAll(\"input\"); for (var i=0; i<inputs.length; i++) { inputs[i].value = \'' + text + '\'' + '}'
    print(script)
    return script

def get_fill_all_textarea_script(text):
    string = 'var inputs = document.querySelectorAll("textarea"); for (var i=0; i<inputs.length; i++) { inputs[i].value = \'' + text + '\'' + '}'
    return string


def is_document_ready(driver):
    try:
        return "complete" == driver.execute_script("return document.readyState")
    except WebDriverException:
        pass


def wait_for_document_ready(driver):
    try:
        WebDriverWait(driver, 5, 0.2).until(is_document_ready, 'document ready')
    except TimeoutException:
        pass


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass


def wait_for_ajax_complete(driver):
    try:
        WebDriverWait(driver, 10, 0.5).until(ajax_complete, 'AJAX')
    except TimeoutException:
        pass

def wait_for_head_load(driver):
    BODY = 'body'
    WebDriverWait(driver, 10, 0.1).until(
            lambda d: d.find_elements_by_css_selector(BODY)
    )


def fill_all_text_field(driver, text):

    fill_all_input = 'var inputs = document.querySelectorAll("input"); ' \
                 'for (var i=0; i<inputs.length; i++) {' \
                    'inputs[i].value = "' + text + '"' + '}'

    fill_all_textarea = 'var inputs = document.querySelectorAll("textarea"); ' \
                 'for (var i=0; i<inputs.length; i++) {' \
                    'inputs[i].value = "' + text + '"' + '}'

    driver.execute_script(fill_all_input)
    driver.execute_script(fill_all_textarea)
