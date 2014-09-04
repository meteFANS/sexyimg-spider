#!/usr/bin/python  
# -*- coding:utf-8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem

import re


__author__ = 'jeff'


class My5542Spider(CrawlSpider):
    name = '5542'

    download_delay = 0
    allowed_domains = ['5542.cc']

    start_urls = ['http://www.5542.cc']

    rules = [
        Rule(SgmlLinkExtractor(allow='/.*(html)$', unique=True), callback='parse_item',
             follow=True)
    ]


    def parse_item(self, response):
        sel = Selector(response)

        name = ''.join([n.encode('utf-8') for n in sel.xpath('//div[@class="title"]/h1/text()').extract()])
        name = name.strip()
        # 温柔白嫩的性感女神私房写真(2)
        if re.match(r'.*(\(\d+\))$', name) is not None:
            name = name[:name.rfind('(')]

        imgs = sel.xpath('//div[@class="content"]//img/@src').extract()

        item = SexyimgItem()
        item['name'] = name.strip()
        item['urls'] = [n.encode('utf-8') for n in imgs]
        item['domain'] = 'http://www.5542.cc/'
        item['page'] = response.url

        yield item