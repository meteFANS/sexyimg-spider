#!/usr/bin/python  
# -*- coding:utf-8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem
from scrapy import log

__author__ = 'jeff'


class Tu567Spider(CrawlSpider):
    name = 'Tu567Spider'

    download_delay = 1
    allowed_domains = ['tu567.com']

    start_urls = ['http://www.tu567.com']

    rules = [
        Rule(SgmlLinkExtractor(allow='/mm', unique=True), callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        sel = Selector(response)

        img_results2 = sel.xpath('//div[@id="content"]')

        for i in img_results2:
            item = SexyimgItem()
            item['name'] = ''.join([n.encode('utf-8') for n in i.xpath('//div[@class="title"]/h1/text()').extract()])
            item['urls'] = [n.encode('utf-8') for n in i.xpath('//ul[@id="pictureurls"]//img/@src').extract()]
            item['domain'] = 'http://www.tu567.com/'
            item['page'] = response.url
            log.msg('fetch %d images from %s' % (len(item['urls']), response.url), level='INFO')
            yield item