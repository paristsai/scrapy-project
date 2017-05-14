# -*- coding: utf-8 -*-

import scrapy
from scrapy.conf import settings
from scrapy.http import Request, FormRequest
from cafenomad.items import CafeItem
import random, json
# from yelp_conf import cusine_types, taiwan_cities
from urllib import urlencode

def stripForList(l):
    l = l or []
    return [e.strip() for e in l]
def stripText(s):
    return s.strip() if s else s

class CafeMonadSpider(scrapy.Spider):
    name = "cafenomad"
    def __init__(self, CITY=None, *args, **kwargs):
        super(CafeMonadSpider, self).__init__(*args, **kwargs)
        with open('proxy_list3.txt', 'r') as f:
            self.proxy_pool = f.read().split('\n')
        self.cities = ['taipei']
        print(self.cities)
    def start_requests(self):
        for city in self.cities:
            print("Parsing ...{}".format(city))
            proxy = random.choice(self.proxy_pool)
            target_page = 'https://cafenomad.tw/{}/list'.format(city)
            params = {
                'city': city
            }
            yield FormRequest(url=proxy, method='post', formdata={'data': target_page}, callback=self.parseList, meta={'params': params})
        
    def parseInfo(self, response):
        cafe = response.meta['item']

        tags = response.xpath('//div[@class="modal-body"]/div[@class="row"]/div/a[@class="cafe-tag"]/text()').extract()
        tags = [tag.strip() for tag in tags if len(tag.strip()) > 0]

        address = response.xpath('//div[@class="row"]/div[@class="col-xs-12"]/div/a[@class="btn btn-sm btn-success"]/@href').extract_first()
        address = address.replace('https://www.google.com/maps/place/', '') if address else ''
        
        cafe['tags'] = tags
        cafe['address'] = address

        item = CafeItem(cafe)
        yield item

    def parseList(self, response):
        for sel in response.xpath('//tbody[@class="list"]/tr'):
            cafe = {}
            cafe['id'] = sel.xpath('@id').extract_first()
            cafe['url'] = 'https://cafenomad.tw/ajax/modal/{}'.format(cafe['id'])
            cafe['city'] = response.meta['params']['city']
            for i in range(0, 18):
                key = 'c{}'.format(i)
                c_xpath = './/td[contains(@class, "{} ")]/text()'.format(key)
                if i == 0:
                    name_list = sel.xpath(c_xpath).extract()
                    cafe['name'] = ''.join([name.strip() for name in name_list])
                else:
                    cafe[key] = sel.xpath(c_xpath).extract_first()

            if cafe['id']:
                proxy = random.choice(self.proxy_pool)
                yield FormRequest(url=proxy, method='post', formdata={'data': cafe['url']}, callback=self.parseInfo, meta={'item': cafe})
            else:
                item = CafeItem()
                yield item

        