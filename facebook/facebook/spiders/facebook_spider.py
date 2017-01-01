# -*- coding: utf-8 -*-

import scrapy
from scrapy.conf import settings
from scrapy.http import Request
from facebook.items import FacebookItem

import json

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    def __init__(self, PAGE=None, *args, **kwargs):
        super(FacebookSpider, self).__init__(*args, **kwargs)
        # 全家 152341009257; 7-11 145649977189
        self.page_id = PAGE

    def start_requests(self):
        base_url = 'https://graph.facebook.com/v2.8/{page_id}/feed?access_token={token}'
        fields = '&fields={}'.format(','.join(['message', 'created_time','story', 'shares', 'likes.limit(0).summary(true)', 'comments.limit(0).summary(true)']))
        url = base_url + fields
        # facebook token
        token = ''
        if self.page_id:
            return [Request(url=url.format(page_id=self.page_id, token=token), method='get', callback=self.parse)]
        else:
            print("Please input facebook page id.")
            return []

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        data = jsonresponse.get('data', [])
        next_page = jsonresponse.get('paging', {}).get('next', None)
        for post in jsonresponse.get('data', []):
            post['likes'] = post.get('likes', {}).get('summary', {}).get('total_count', 0)
            post['comments'] = post.get('comments', {}).get('summary', {}).get('total_count', 0)
            post['shares'] = post.get('shares', {}).get('count', 0)
            item = FacebookItem(post)
            yield item

        if next_page is not None:
            print("next page: {}".format(next_page))
            yield scrapy.Request(next_page, callback=self.parse)
