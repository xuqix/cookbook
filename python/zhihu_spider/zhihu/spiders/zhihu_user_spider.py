# -*- coding:utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from zhihu.items import ZhihuUser

from scrapy.http import Request,FormRequest
from zhihu.settings import *

from zhihu.helper import helper
import termcolor
import re, json
from urllib import urlencode

import sys, random, time, datetime
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
                'password':'xxxxxxx',
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
        #if len(ar)==0: return
        #s="\n" + prefix + "\n".join(ar)
        #open('crawl.txt', 'a').write(s)
        for a in ar:
            print(a)

    def parse_user(self, response):
        sel = Selector(response)
        user = ZhihuUser()
        user['_id'] = user['username'] = response.url.split('/')[-2]
        #url
        user['url'] = response.url
        #nick
        user['nickname'] = ''.join(sel.xpath('//a[@class="name"]/text()').extract())
        #bio
        user['bio'] = ''.join(sel.xpath('//span[@class="bio"]/text()').extract())
        #localtion
        user['location'] = ''.join(sel.xpath('//span[@class="location item"]/@title').extract())
        #employment
        user['employment'] = ''.join(sel.xpath('//span[@class="employment item"]/a/text()').extract())
        #position
        user['position'] = ''.join(sel.xpath('//span[@class="position item"]/@title').extract())
        #edu
        scho = ''.join(sel.xpath('//span[@class="education item"]/a/text()').extract())
        ext = ''.join(sel.xpath('//span[@class="education-extra item"]/@title').extract())
        user['education'] = scho + ' ' + ext
        #followe
        res = sel.xpath("//a[@class='item']/strong/text()").extract()
        followee_num =user['followee'] = res[0]
        follower_num = user['follower']= res[1]
        #profile [赞同, 感谢, 收藏, 分享]
        res = (sel.xpath('//div[@class="zm-profile-module-desc"]/span/strong/text()').extract())
        user['agree']   = res[0]
        user['thanks']  = res[1]
        user['fav'] = res[2]
        user['share']   = res[3]
        #[提问, 回答, 文章, 收藏, 公共编辑]
        res = sel.xpath("//div[@class='profile-navbar clearfix']/a[@class='item ']/span/text()").extract()
        if len(res) ==5:
            user['ask'] = res[0]
            user['answer'] = res[1]
            user['post'] = res[2]
            user['collection'] = res[3]
            user['log'] = res[4]
        #update time
        user['update_time'] = str(datetime.datetime.now())
        yield user

        #self.dbg(response)

        num = int(followee_num) if followee_num else 0
        page_num = num/20 + (1 if num%20 else 0)
        page_num = 1
        hash_id = ''.join(sel.xpath('//div[@class="zm-profile-header-op-btns clearfix"]/button/@data-id').extract())
        for i in xrange(page_num):
            params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":i*20})
            payload = {"method":"next", "params": params} #, "_xsrf":self._xsrf}
            yield Request("https://www.zhihu.com/node/ProfileFolloweesListV2?"+urlencode(payload),
                    meta={'cookiejar':1}, headers=self.headers)
                    #callback=self.parse_follow_url)
        return

        num = int(follower_num) if follower_num else 0
        page_num = num/20 + (1 if num%20 else 0)
        for i in xrange(page_num):
            params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":i*20})
            payload = {"method":"next", "params": params} #, "_xsrf":_xsrf}
            yield Request("http://www.zhihu.com/node/ProfileFollowersListV2?"+urlencode(payload),
                    meta={'cookiejar':1}, headers=self.headers)
                    #callback=self.parse_follow_url)
        #url = re.sub('about$', 'followees', response.url)
        #url = re.sub('https:', 'http:', url)
        #yield Request(url, meta={'cookiejar':1}, headers=self.headers)

    def dbg(self, response):
        #start debug shell
        from scrapy.shell import inspect_response
        inspect_response(response, self)

