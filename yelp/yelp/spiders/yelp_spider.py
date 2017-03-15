# -*- coding: utf-8 -*-

import scrapy
from scrapy.conf import settings
from scrapy.http import Request, FormRequest
from yelp.items import YelpItem
import random, json
from yelp_conf import cusine_types, taiwan_cities
from urllib import urlencode

def stripForList(l):
    l = l or []
    return [e.strip() for e in l]
def stripText(s):
    return s.strip() if s else s

class YelpSpider(scrapy.Spider):
    name = "yelp"
    def __init__(self, PAGE=None, *args, **kwargs):
        super(YelpSpider, self).__init__(*args, **kwargs)
        with open('proxy_list3.txt', 'r') as f:
            self.proxy_pool = f.read().split('\n')
        self.domain = 'https://www.yelp.com.tw'
        self.cities = taiwan_cities
        self.cusine_types = cusine_types

        self.search_base_url = self.domain + '/search?'
        self.start = 0
    def start_requests(self):
        # proxy = random.choice(self.proxy_pool)
        # params = {
        #     'find_loc': self.cities[0],
        #     'cflt': 'belgian',
        #     'start': self.start
        # }
        # target_page = self.search_base_url + urlencode(params)
        # print(target_page)
        # yield FormRequest(url=proxy, method='post', formdata={'data': target_page}, callback=self.parseList, meta={'params': params})

        for city in self.cities[:1]:
            for cusine in self.cusine_types:
                params = {
                    'find_loc': city,
                    'cflt': cusine,
                    'start': self.start
                }
                target_page = self.search_base_url + urlencode(params)
                print("Parsing ...{}".format(target_page))
                proxy = random.choice(self.proxy_pool)
                yield FormRequest(url=proxy, method='post', formdata={'data': target_page}, callback=self.parseList, meta={'params': params})
        

    def parseInfo(self, response):
        biz = response.meta['item']
        opening_time = {}
        for sel in response.xpath('//table[@class="table table-simple hours-table"]/tbody/tr'):
            opening_time.setdefault(sel.xpath('.//th[@scope="row"]/text()').extract_first() or '', sel.xpath('.//td/span[@class="nowrap"]/text()').extract())

        biz['address'] = stripForList(response.xpath('//strong[@class="street-address"]/address/text()').extract())
        map_directions = response.xpath('//a[@class="biz-map-directions"]/img/@src').re_first(r'center=[^\&]+')
        biz['latitude'] = map_directions.split('%2C')[0].replace('center=', '') if map_directions else None
        biz['longitude'] = map_directions.split('%2C')[1] if map_directions else None
        biz['price_description'] = stripText(response.xpath('//dd[@class="nowrap price-description"]/text()').extract_first())
        biz['website'] = response.xpath('//span[contains(@class, "biz-website")]/a/text()').extract_first()
        biz['related_businesses'] = response.xpath('//div[@class="ywidget related-businesses js-related-businesses"]/ul/li/div/div[@class="media-story"]/div/a/span/text()').extract()
        biz['yelp_reserve'] = True if response.xpath('//div[contains(@class, "reservations")]') else False

        attr_sel = response.xpath('//div[@class="ywidget"]')
        if attr_sel:
            attr_sel = attr_sel[0]
            attr_dict = {}
            for sub_sel in attr_sel.xpath('.//ul/li/div/dl'):
                attr_key = sub_sel.xpath('.//dt/text()').extract_first().strip()
                attr_val = sub_sel.xpath('.//dd/text()').extract_first().strip()
                attr_dict[attr_key] = attr_val
            biz['attributes'] = json.dumps(attr_dict)
        item = YelpItem(biz)
        yield item

    def parseList(self, response):
        for sel in response.xpath('//ul[@class="ylist ylist-bordered search-results"]/li/*'):
            biz = {}
            biz['name'] = sel.xpath('.//a[@class="biz-name js-analytics-click"]/span/text()').extract_first()
            biz['url'] = sel.xpath('.//a[@class="biz-name js-analytics-click"]/@href').extract_first()
            biz['url'] = (self.domain + biz['url']) if biz['url'] else None
            biz['alternate_name'] = sel.xpath('.//span[@class="biz-alternate-names"]/text()').extract_first()
            biz['stars'] = stripText(sel.xpath('.//div[contains(@class, "i-stars") and contains(@class, "rating-large")]/@title').re_first(r'[0-9\.]+'))
            biz['review_num'] = stripText(sel.xpath('.//span[@class="review-count rating-qualifier"]/text()').re_first(r'[0-9]+'))
            biz['price_range'] = sel.xpath('.//span[@class="business-attribute price-range"]/text()').extract_first()
            biz['category_list'] = sel.xpath('.//span[@class="category-str-list"]/a/text()').extract()
            biz['neighborhood_list'] = stripText(sel.xpath('.//span[@class="neighborhood-str-list"]/text()').extract_first())
            biz['phone'] = stripText(sel.xpath('.//span[@class="biz-phone"]/text()').extract_first())
            biz['search_result_tags'] = stripForList(sel.xpath('.//ul[@class="search-result_tags"]/li/small/text()').re(r'\w+'))

            if biz['url']:
                proxy = random.choice(self.proxy_pool)
                yield FormRequest(url=proxy, method='post', formdata={'data': biz['url']}, callback=self.parseInfo, meta={'item': biz})
            else:
                item = YelpItem()
                yield item

        next_page = response.xpath('//span[@class="pagination-label responsive-hidden-small pagination-links_anchor"]/text()').extract_first()
        if next_page == u'\u4e0b\u4e00\u9801':
            proxy = random.choice(self.proxy_pool)

            params = response.meta['params']
            params['start'] += 10
            target_page = self.search_base_url + urlencode(params)
            print("Parsing ...{}".format(target_page))
            yield FormRequest(url=proxy, method='post', formdata={'data': target_page}, callback=self.parseList, meta={'params': params})
