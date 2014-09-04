#!/usr/bin/python  
# -*- coding:utf-8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sexyimg.items import SexyimgItem
from scrapy import log


class PaopaowoSpider(CrawlSpider):
    name = 'PaopaowoSpider'

    download_delay = 1
    allowed_domains = ['paopaowo.com']

    start_urls = ['http://www.paopaowo.com']

    rules = [
        Rule(SgmlLinkExtractor(allow='/.*(shtml)$', unique=True), callback='parse_item',
             follow=True)
    ]


    def parse_item(self, response):
        print 'prase: %s' % response.url
        sel = Selector(response)

        name = [n.encode('utf-8') for n in sel.xpath('//div[@class="biaoti"]/div[@class="l"]/text()').extract()]

        imgs = sel.xpath('//div[@id="eData"]/dl/dd/text()').extract()

        print imgs

        item = SexyimgItem()
        item['name'] = ''.join(name)
        item['urls'] = [n.encode('utf-8') for n in imgs]
        item['domain'] = 'http://www.paopaowo.com'
        item['page'] = response.url
        log.msg('fetch %d images from %s' % (len(item['urls']), response.url), level='INFO')
        yield item