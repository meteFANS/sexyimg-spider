#!/usr/bin/python  
# -*- coding:utf-8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem
from scrapy import log
import re

__author__ = 'jeff'


class Simei8Spider(CrawlSpider):
    ''' fetch images from http://www.simei8.com'''
    name = 'Simei8Spider'

    download_delay = 1
    allowed_domains = ['simei8.com']

    start_urls = ['http://www.simei8.com']

    rules = [
        Rule(SgmlLinkExtractor(allow='/html', unique=True), callback='parse_item',
             follow=True)
    ]


    def parse_item(self, response):
        sel = Selector(response)

        name = ''.join([n.encode('utf-8') for n in sel.xpath('//div[@id="ctt"]/h1/text()').extract()])

        if name.find('-') > -1:
            name = name[:name.rfind('-')]

        imgs = sel.xpath('//div[@class="pp"]/a/img/@src').extract()

        item = SexyimgItem()
        item['name'] = name
        item['domain'] = 'http://www.simei8.com/'
        item['page'] = response.url
        item['urls'] = [n.encode('utf-8') for n in imgs]

        log.msg('fetch %d images from %s' % (len(item['urls']), response.url), level='INFO')

        yield item
