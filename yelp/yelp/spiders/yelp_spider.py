# -*- coding: utf-8 -*-

import scrapy
from scrapy.conf import settings
from scrapy.http import Request, FormRequest
from yelp.items import YelpItem
import random

class YelpSpider(scrapy.Spider):
    name = "yelp"
    def __init__(self, PAGE=None, *args, **kwargs):
        super(YelpSpider, self).__init__(*args, **kwargs)
        self.proxy_pool = ['http://proxy2-1262.appspot.com/proxy', 'http://proxy3-1262.appspot.com/proxy', 'http://proxy4-1262.appspot.com/proxy', 'http://proxy5-1262.appspot.com/proxy', 'http://proxy6-1262.appspot.com/proxy', 'http://proxy7-1262.appspot.com/proxy', 'http://proxy8-1262.appspot.com/proxy']
        self.domain = 'https://www.yelp.com.tw'
        self.search_base_url = self.domain + '/search?find_loc=%E5%8F%B0%E5%8C%97%E5%B8%82&start={}&cflt=restaurants'
        self.page = 1
    def start_requests(self):
        proxy = random.choice(self.proxy_pool)
        next_page = self.search_base_url.format((self.page - 1)*10)
        return [FormRequest(url=proxy, method='post', formdata={'data': next_page}, callback=self.parseList)]

    def parseInfo(self, response):
        biz = response.meta['item']
        # biz['opening_time'] = 
        biz['price_description'] = response.xpath('//dd[@class="nowrap price-description"]/text()').re_first(r'\$[0-9-]+')
        item = YelpItem(biz)
        yield item

    def parseList(self, response):
        for sel in response.xpath('//ul[@class="ylist ylist-bordered search-results"]/li/*'):
            biz = {}
            biz['name'] = sel.xpath('.//a[@class="biz-name js-analytics-click"]/span/text()').extract_first()
            biz['url'] = sel.xpath('.//a[@class="biz-name js-analytics-click"]/@href').extract_first()
            biz['url'] = (self.domain + biz['url']) if biz['url'] else None
            biz['alternate_name'] = sel.xpath('.//span[@class="biz-alternate-names"]/text()').extract_first()

            if biz['url']:
                proxy = random.choice(self.proxy_pool)
                yield FormRequest(url=proxy, method='post', formdata={'data': biz['url']}, callback=self.parseInfo, meta={'item': biz})
            else:
                item = YelpItem()
                yield item


        # if self.page <= 100:
        #     proxy = random.choice(self.proxy_pool)
        #     self.page += 1
        #     next_page = self.base_url.format((self.page - 1)*10)
        #     print("next page: {}".format(self.page))
        #     yield FormRequest(url=proxy, method='post', formdata={'data': next_page}, callback=self.parseList)
