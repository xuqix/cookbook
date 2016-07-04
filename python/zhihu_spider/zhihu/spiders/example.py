from scrapy.spiders import Spider
from scrapy.selector import Selector

from zhihu.items import ZhihuItem

from scrapy.http import Request,FormRequest
from zhihu.settings import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ExampleSpider(Spider):
    name = "example"
    allowed_domains = ["zhihu.com"]

    start_urls = [ "http://www.zhihu.com/explore", ]

    def __init__(self):
        self.headers = HEADER
        self.cookies = COOKIES

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
              yield FormRequest(url, meta = {'cookiejar': i},  headers = self.headers,
                      cookies =self.cookies, callback = self.parse)#jump to login page

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="explore-feed feed-item"]')
        for site in sites:
            for s in (site.xpath('h2/a[@class="question_link"]/text()').extract()):
                print s.encode('utf-8')
        return []

