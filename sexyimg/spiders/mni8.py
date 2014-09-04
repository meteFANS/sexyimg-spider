#!/usr/bin/python  
# -*- coding:utf-8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem
from scrapy import log

__author__ = 'jeff'


class Mni8Spider(CrawlSpider):
    name = 'Mni8Spider'

    download_delay = 1
    allowed_domains = ['mni8.com']

    start_urls = ['http://www.mni8.com/']

    rules = [
        Rule(SgmlLinkExtractor(allow='/.*(html)$', unique=True), callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        print 'prase: %s' % response.url
        sel = Selector(response)

        tmpname = [n.encode('utf-8') for n in sel.xpath('//div[@class="article_img_mid"]/h1/text()').extract()]
        url = [n.encode('utf-8') for n in sel.xpath('//img[@id="bigimg"]/@src').extract()]

        name = ''.join(tmpname)
        name = name[:name.rfind('(')]

        item = SexyimgItem()
        item['name'] = name
        item['urls'] = url
        item['domain'] = 'http://www.mni8.com/'
        item['page'] = response.url

        log.msg('fetch %d images from %s' % (len(item['urls']), response.url), level='INFO')

        yield item


