# -*- coding=utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector

from zhihu.items import ZhihuItem

from scrapy.http import Request,FormRequest
from zhihu.settings import *

from zhihu.helper import helper

import sys, random
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

    def log(self, s):
        helper.Logger.debug(s)

    def start_requests(self):
        return [Request("http://www.zhihu.com", headers = self.headers, meta={"cookiejar":1}, callback = self.post_login)]

    def post_login(self, response):
        self.log('正在登陆...')
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        captcha = helper.get_captcha("https://www.zhihu.com/captcha.gif", params={"r":random.random(), "type":"login"}, headers=self.headers)
        return [FormRequest(
            "http://www.zhihu.com/login/phone_num",
            formdata = {
                '_xsrf':'zzzzzzzzzzz',
                'password':'xxxxx',
                'remember_me':'true',
                'phone_num':'yyyyy',
                'captcha':captcha,
            },
            meta={'cookiejar':response.meta['cookiejar']},
            headers = HEADER,
            callback = self.after_login
        )]

    def after_login(self, response):
        r = eval(response.text)
        self.log(unicode(r['msg'],'unicode-escape'))
        if r['r'] != 0: return
        for url in self.start_urls:
            yield Request(url, meta={'cookiejar':1}, headers=self.headers)
            #yield self.make_requests_from_url(url)

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="explore-feed feed-item"]')
        for site in sites:
            for s in (site.xpath('h2/a[@class="question_link"]/text()').extract()):
                print s
        open('test.html', 'w').write(response.text.encode('utf-8'))
        return []

