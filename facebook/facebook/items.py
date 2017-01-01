# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FacebookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	id = scrapy.Field()
	story = scrapy.Field()
	message = scrapy.Field()
	created_time = scrapy.Field()
	likes = scrapy.Field()
	comments = scrapy.Field()
	shares = scrapy.Field()