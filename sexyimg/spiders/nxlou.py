#!/usr/bin/python  
# -*- coding:utf-8 -*-
import re
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem


class NxlouSpider(CrawlSpider):
    name = 'NxlouSpider'

    download_delay = 0
    allowed_domains = ['tuku.nxlou.com']

    start_urls = ['http://tuku.nxlou.com/']

    rules = [
        Rule(SgmlLinkExtractor(allow='/.*(html)$', unique=True), callback='parse_item',
             follow=True)
    ]


    def parse_item(self, response):
        print response.url

        sel = Selector(response)

        name = ''.join([n.encode('utf-8') for n in sel.xpath('//h1[@class="yh"]/a/text()').extract()])
        name = name.strip()

        if re.match(r'.+\(\d+\)$', name) is not None:
            name = name[:name.rfind('(')]

        imgs = sel.xpath('//table//a/img/@src').extract()

        item = SexyimgItem()
        item['name'] = name.strip()
        item['urls'] = [n.encode('utf-8') for n in imgs]
        item['domain'] = 'http://tuku.nxlou.com/'
        item['page'] = response.url

        yield item