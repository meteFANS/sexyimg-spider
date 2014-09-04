#!/usr/bin/python  
# -*- coding:utf-8 -*-
import re
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem

__author__ = 'jeff'


class LinlinSpider(CrawlSpider):
    name = "LinlinSpider"

    download_delay = 0
    allowed_domains = ['mm.linlin.com']

    start_urls = ['http://mm.linlin.com']

    rules = [
        Rule(SgmlLinkExtractor(allow='/.*(html)$', unique=True), callback='parse_item',
             follow=True)
    ]


    def parse_item(self, response):
        sel = Selector(response)

        name = ''.join([n.encode('utf-8') for n in sel.xpath('//h1[@class="mn_title"]/text()').extract()])
        name = name.strip()
        if re.match(r'.*(\(\d+\))$', name) is not None:
            name = name[:name.rfind('(')]
        name = name.strip()

        imgs = sel.xpath('//div[@class="mnvimg"]//img/@src').extract()

        item = SexyimgItem()
        item['name'] = name.strip()
        item['urls'] = [n.encode('utf-8') for n in imgs]
        item['domain'] = 'http://mm.linlin.com/'
        item['page'] = response.url

        yield item






