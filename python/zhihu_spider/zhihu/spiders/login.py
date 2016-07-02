from scrapy.spiders import Spider
from scrapy.selector import Selector

from zhihu.items import ZhihuItem

from scrapy.http import Request,FormRequest
from zhihu.settings import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LoginSpider(Spider):
    name = "login"
    allowed_domains = ["zhihu.com"]

    start_urls = [
            "http://www.zhihu.com/explore",
            #"https://www.zhihu.com",
            ]

    def __init__(self):
        self.headers = HEADER
        self.cookies = COOKIES

    def start_requests(self):
        return [FormRequest(
            "http://www.zhihu.com/login/phone_num",
            formdata = {
                '_xsrf':'zzzzzzzzzzz',
                'password':'xxxxx',
                'remember_me':'true',
                'phone_num':'yyyyy',
            },
            headers = HEADER,
            cookies = COOKIES,
            callback = self.after_login
        )]

    def after_login(self, response):
        r = eval(response.text)
        print unicode(r['msg'],'unicode-escape')
        if r['r'] != 0: return
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="explore-feed feed-item"]')
        for site in sites:
            for s in (site.xpath('h2/a[@class="question_link"]/text()').extract()):
                print s
        open('test.html', 'w').write(response.text.encode('utf-8'))
        return []

