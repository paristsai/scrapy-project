# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    alternate_name = scrapy.Field()
    url = scrapy.Field()
    stars = scrapy.Field()
    review_num = scrapy.Field()
    price_range = scrapy.Field()
    price_description = scrapy.Field()
    category_list = scrapy.Field()
    neighborhood_list = scrapy.Field()
    address1 = scrapy.Field()
    address2 = scrapy.Field()
    phone = scrapy.Field()
    search_result_tags = scrapy.Field()
    reserve = scrapy.Field()
    opening_time = scrapy.Field()
    reservable = scrapy.Field()
    delivery = scrapy.Field()
    takeout = scrapy.Field()
    suitable = scrapy.Field()
    children = scrapy.Field()
    groups = scrapy.Field()
    clothing = scrapy.Field()
    atmosphere = scrapy.Field()
    noise = scrapy.Field()
    alcohol = scrapy.Field()
    outdoor_seating = scrapy.Field()
    wifi = scrapy.Field()
    tv = scrapy.Field()
    waiter_service = scrapy.Field()
    host_banquet = scrapy.Field()
    related_businesses = scrapy.Field()