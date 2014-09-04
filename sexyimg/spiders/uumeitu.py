#!/usr/bin/python  
# -*- coding:utf-8 -*-
import re
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem

__author__ = 'jeff'


class UumeituSpider(CrawlSpider):
    name = 'UumeituSpider'

    download_delay = 1
    allowed_domains = ['uumeitu.com']

    start_urls = ['http://www.uumeitu.com/']

    rules = [
        Rule(SgmlLinkExtractor(allow='/a/.*(html)$', unique=True), callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        print 'prase: %s' % response.url
        sel = Selector(response)

        name = ''.join([n.encode('utf-8') for n in sel.xpath('//div[@class="title"]/h2/text()').extract()])
        name = name.strip()

        if re.match(r'.*\(\d+\)$', name) is not None:
            name = name[:name.rfind('(')]

        imgs = sel.xpath('//div[@class="content"]//img/@src').extract()

        item = SexyimgItem()
        item['name'] = name.strip()
        item['urls'] = [n.encode('utf-8') for n in imgs]
        item['domain'] = 'http://www.uumeitu.com/'
        item['page'] = response.url

        yield item