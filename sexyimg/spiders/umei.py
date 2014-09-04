#!/usr/bin/python  
# -*- coding:utf-8 -*-
import re
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem

__author__ = 'jeff'


class UmeiSpider(CrawlSpider):
    name = 'UmeiSpider'

    download_delay = 0
    allowed_domains = ['umei.cc']

    start_urls = ['http://www.umei.cc/']

    rules = [
        Rule(SgmlLinkExtractor(allow='/p/.*(htm)$', unique=True), callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        sel = Selector(response)

        name = ''.join([n.encode('utf-8') for n in sel.xpath('//div[@id="content"]//h2/text()').extract()])
        name = name.strip()

        if re.match(r'.*\(\d+\)$', name) is not None:
            name = name[:name.rfind('(')]

        imgs = sel.xpath('//div[@class="img_box"]//img/@src').extract()

        item = SexyimgItem()
        item['name'] = name.strip()
        item['urls'] = [n.encode('utf-8') for n in imgs]
        item['domain'] = 'http://www.umei.cc/'
        item['page'] = response.url

        yield item