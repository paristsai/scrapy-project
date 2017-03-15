# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    alternate_name = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()
    stars = scrapy.Field()
    review_num = scrapy.Field()
    price_range = scrapy.Field()
    price_description = scrapy.Field()
    category_list = scrapy.Field()
    neighborhood_list = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    phone = scrapy.Field()
    search_result_tags = scrapy.Field()
    opening_time = scrapy.Field()
    yelp_reserve = scrapy.Field()
    related_businesses = scrapy.Field()
    attributes = scrapy.Field()
    # reservable = scrapy.Field()
    # delivery = scrapy.Field()
    # takeout = scrapy.Field()
    # suitable = scrapy.Field()
    # children = scrapy.Field()
    # groups = scrapy.Field()
    # clothing = scrapy.Field()
    # atmosphere = scrapy.Field()
    # noise = scrapy.Field()
    # alcohol = scrapy.Field()
    # outdoor_seating = scrapy.Field()
    # wifi = scrapy.Field()
    # tv = scrapy.Field()
    # waiter_service = scrapy.Field()
    # host_banquet = scrapy.Field()
    