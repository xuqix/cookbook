# -*- coding:utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from zhihu.items import ZhihuItem

from scrapy.http import Request,FormRequest
from zhihu.settings import *

from zhihu.helper import helper
import termcolor
import re

import sys, random, time
reload(sys)
sys.setdefaultencoding('utf-8')

class UserInfoSpider(CrawlSpider):
    name = "user_info"
    allowed_domains = ["zhihu.com"]

    start_urls = [
            "http://www.zhihu.com/explore",
            #"https://www.zhihu.com",
            ]

    rules = (
        Rule(LinkExtractor(
            allow=("/people/[a-zA-Z0-9-_/]+", ), restrict_xpaths=('//div[@class="top-nav-profile"]/ul/li/a')),
            follow=True,
            process_request = 'request_with_cookie',
            process_links = 'home_links',
            callback='parse_item'),

        Rule(LinkExtractor(
            allow=("/people/[a-zA-Z0-9-_/]+", ), restrict_xpaths=('//div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]/a[@class="zm-item-link-avatar"]')),
            follow=True,
            process_request = 'request_with_cookie',
            process_links = 'about_links',
            callback='parse_user'),
    )

    def request_with_cookie(self, r):
        r = r.replace(headers=self.headers)
        r.meta.update({"cookiejar":1})
        return r

    def home_links(self, links):
        for l in links: l.url += '/followees'
        return links
    def about_links(self, links):
        for l in links: l.url += '/about'
        return links

    def __init__(self, *a, **kwargs):
        super(UserInfoSpider, self).__init__(*a, **kwargs)
        self.headers = HEADER
        self.cookies = COOKIES

    def log(self, s):
        helper.Logger.debug(s)

    def start_requests(self):
        return [Request("http://www.zhihu.com", headers = self.headers, meta={"cookiejar":1}, callback = self.get_captcha)]

    def get_captcha(self, response):
        self._xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        return Request(
                'http://www.zhihu.com/captcha.gif?r='+str(int(time.time()*1000))+'&type=login',
                meta={'cookiejar':response.meta['cookiejar']},
                headers = self.headers,
                callback=self.post_login)

    def post_login(self, response):
        self.log('正在登陆...')
        return [FormRequest(
            "http://www.zhihu.com/login/phone_num",
            formdata = {
                '_xsrf':self._xsrf,
                'password':'xxxxx',
                'remember_me':'true',
                'phone_num':'yyyyyy',
                'captcha':helper.gen_captcha(response.body, response.headers['content-type'].split('/')[1]),
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

    def parse_item(self, response):
        sel = Selector(response)
        #for l in sel:
            #self.log(l.url)
        return []

    def pr(self, ar, prefix=''):
        if len(ar)==0: return
        s="\n" + prefix + "\n".join(ar)
        open('crawl.txt', 'a').write(s)
        #for a in ar:
            #print(a)

    def parse_user(self, response):
        sel = Selector(response)
        #url
        self.pr([response.url])
        #nick
        self.pr(sel.xpath('//a[@class="name"]/text()').extract(), '昵称:')
        #bio
        self.pr(sel.xpath('//span[@class="bio"]/text()').extract(), '简介:')
        #localtion
        self.pr(sel.xpath('//span[@class="location item"]/@title').extract(), '居住地:')
        #employment
        self.pr(sel.xpath('//span[@class="employment item"]/a/text()').extract(), '公司:')
        #position
        self.pr(sel.xpath('//span[@class="position item"]/@title').extract(), '职业:')
        #edu
        self.pr(sel.xpath('//span[@class="education item"]/a/text()').extract(), '教育经历:')
        self.pr(sel.xpath('//span[@class="education-extra item"]/@title').extract())
        #profile
        desc = ['赞同', '感谢', '收藏', '分享']
        res = (sel.xpath('//div[@class="zm-profile-module-desc"]/span/strong/text()').extract())
        for i, e in enumerate(res): res[i] = desc[i]+e
        self.pr(res)

        self.pr(["\n\n"])
        #self.dbg(response)
        url = re.sub('about$', 'followees', response.url)
        url = re.sub('https:', 'http:', url)
        print url
        return Request(url, meta={'cookiejar':1}, headers=self.headers)
        return []

    #def parse(self, response):
        #sel = Selector(response)
        #sites = sel.xpath('//div[@class="explore-feed feed-item"]')
        #for site in sites:
            #for s in (site.xpath('h2/a[@class="question_link"]/text()').extract()):
                #print s
        #open('test.html', 'w').write(response.text.encode('utf-8'))
        #return []

    def dbg(self, response):
        #start debug shell
        from scrapy.shell import inspect_response
        inspect_response(response, self)

