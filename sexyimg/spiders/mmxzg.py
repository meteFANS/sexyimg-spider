#!/usr/bin/python  
# -*- coding:utf-8 -*-
import re
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem

__author__ = 'jeff'


class MmxzgSpider(CrawlSpider):
    name = "MmxzgSpider"

    download_delay = 1
    allowed_domains = ['mmxzg.com']

    start_urls = ['http://www.mmxzg.com']

    rules = [
        Rule(SgmlLinkExtractor(allow='/.*(html)$', unique=True), callback='parse_item',
             follow=True)
    ]


    def parse_item(self, response):
        sel = Selector(response)
        name = ''.join([n.encode('utf-8') for n in sel.xpath('//div[@class="main"]/h1/text()').extract()])
        name = name.strip()

        if re.match(r'.*(\(\d+\))$', name) is not None:
            name = name[:name.rfind('(')]

        imgs = sel.xpath('//ul[@class="ad-thumb-list"]/li/a/@href').extract()

        imgs2 = sel.xpath('//div[@class="main"]/p/a/img[@onload]/@src').extract()

        imgs.extend(imgs2)

        item = SexyimgItem()
        item['name'] = name.strip()
        item['urls'] = [n.encode('utf-8') for n in imgs]
        item['domain'] = 'http://www.mmxzg.com/'
        item['page'] = response.url

        yield item











