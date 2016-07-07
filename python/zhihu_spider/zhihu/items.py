# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ZhihuUser(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id         = Field()
    url         = Field()
    username    = Field()
    nickname    = Field()
    bio         = Field()
    location    = Field()
    employment  = Field()
    position    = Field()
    education   = Field()

    followee    = Field()
    follower    = Field()

    agree       = Field()
    thanks      = Field()
    fav         = Field()
    share       = Field()

    ask         = Field()
    answer      = Field()
    post        = Field()
    collection  = Field()
    log         = Field()

    update_time = Field()

