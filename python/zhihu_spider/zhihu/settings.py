# -*- coding: utf-8 -*-

# Scrapy settings for zhihu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihu'

SPIDER_MODULES = ['zhihu.spiders']
NEWSPIDER_MODULE = 'zhihu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihu (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1 #3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihu.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihu.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zhihu.pipelines.MongoDBPipeline': 200,
    #'zhihu.pipelines.JsonPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

HEADER = {
    "Host": "www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
}

COOKIES = {
    'q_c1':'541e782bbf574552ac483df33c258d41|1466996438000|1466996438000',
    'cap_id':'"YTIxMWQyYWE4MmJhNDFjNGJhYWRiYjkyODgxNWE2Y2Y=|1467441522|a96fa8e7f06532d5cadb8af91567dc575d2210ee"',
    '__utma':'51854390.34320148.1467430131.1467435061 .1467440396.3',
    '__utmz':'51854390.1467440396.3.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct =/explore',
    '_za':'046b5515-9dc3-40a7-91bb-6fcbdab0e30a',
    'udid':'"AJAACOFQlQmPTiHeKYScraK4bFLW9kZwj40=|1457516920" ',
    'l_cap_id':'"NzU3MzU0MDE2NTZmNGUxM2ExY2MyODhiODRjNmE1YjI=|1467441522|4451fb6e192323db8abaa2b4557d4a3f434e3a26"',
    'd_c0':'"AGCAhxNksQmPTrhuHPoHnZwBhiwGVTTiWN0=|1459303326"',
    '_zap':'b96e3f10-e061-4827-b6ca-cac23ff1167c',
    'login':'"ZmY1ODFkMmU5OGIxNGZhMWJmMWU1M2ExYzQ2ZDE4ZTU=|1467441696|cdabf71e3c8130895394f843360f0991c0bdfd8f"',
    '_xsrf':'24098e95fed4031179fbfc31290de3aa',
    '__utmc':'51854390',
    '__utmv':'51854390.000--|2=registration_date =20160702=1^3=entry_date=20160627=1',
    'n_c':'1',
    '__utmb':'51854390.4.10.1467440396',
    '__utmt':'1',
    'a_t':'"2.0AJCABxORKgoXAAAAIO-eVwCQgAcTkSoKAGCAhxNksQkXAAAAYQJVTSDvnlcAKTyuws2cjUL0IbpCsolwHHsAcoOJY9NT0UGNbWf8L6RIrKAyMEGcCw=="',
    'z_c0':'Mi4wQUpDQUJ4T1JLZ29BWUlDSEUyU3hDUmNBQUFCaEFsVk5KdXVlVndCblNVbkFCOHRaY3A2TC1iR2E0MWtXek9aT1l3 |1467440678|4cecb6b7520a9a1b1a17b041616e3906ae502ef6',
}
