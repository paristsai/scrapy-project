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
         # facebook token
        self.token = ''

        base_url = 'https://graph.facebook.com/v2.8/{page_id}/feed?access_token={token}'
        fields = '&fields={}'.format(','.join(['type', 'message', 'created_time','story', 'shares', 'likes.limit(0).summary(true)', 'comments.limit(0).summary(true)', 'object_id']))
        self.feed_url = (base_url + fields).format(page_id=self.page_id, token=self.token)

        self.photo_url = 'https://graph.facebook.com/v2.8/{object_id}/?fields=images&access_token={token}'

    def start_requests(self):
        if self.page_id:
            return [Request(url=self.feed_url, method='get', callback=self.parsePost)]
        else:
            print("Please input facebook page id.")
            return []

    def parsePhoto(self, response):
        post = response.meta['item']

        jsonresponse = json.loads(response.body_as_unicode())
        post['images'] = jsonresponse.get('images', [])
        item = FacebookItem(post)
        yield item

    def parsePost(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        data = jsonresponse.get('data', [])
        next_page = jsonresponse.get('paging', {}).get('next', None)
        for post in jsonresponse.get('data', []):
            post['likes'] = post.get('likes', {}).get('summary', {}).get('total_count', 0)
            post['comments'] = post.get('comments', {}).get('summary', {}).get('total_count', 0)
            post['shares'] = post.get('shares', {}).get('count', 0)

            if post['type'] == 'photo' and post['object_id']:
                yield scrapy.Request(self.photo_url.format(object_id=post['object_id'], token=self.token), callback=self.parsePhoto, meta={'item': post})
            else:
                post['images'] = None
                item = FacebookItem(post)
                yield item

        if next_page is not None:
            print("next page: {}".format(next_page))
            yield scrapy.Request(next_page, callback=self.parsePost)
