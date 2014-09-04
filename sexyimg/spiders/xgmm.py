#!/usr/bin/python  
# -*- coding:utf-8 -*-


from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from sexyimg.items import SexyimgItem


__author__ = 'jeff'


class XgmmSpider(CrawlSpider):
    ''' fetch images from http://www.xgmm.cc'''

    name = 'XgmmSpider'

    download_delay = 1
    allowed_domains = ['xgmm.cc']

    start_urls = ['http://www.xgmm.cc']

    rules = [
        Rule(SgmlLinkExtractor(allow='/mm', unique=True), callback='parse_item',
             follow=True)
    ]


    def parse_item(self, response):
        sel = Selector(response)

        img_results2 = sel.xpath('//div[@id="content"]')

        '''
        img_results = sel.xpath('//img[@data-original]')
        for i in img_results:
            item = SexyimgItem()
            item['name'] = self.reformat_string(i.xpath('@alt').extract())
            item['urls'] = [n.encode('utf-8') for n in i.xpath('@data-original').extract()]
            item['domain'] = 'http://www.xgmm.cc/'
            item['page'] = response.url
            yield item
        '''

        for i in img_results2:
            item = SexyimgItem()
            item['name'] = [n.encode('utf-8') for n in i.xpath('//div[@class="title"]/h1/text()').extract()]
            item['urls'] = [n.encode('utf-8') for n in i.xpath('//ul[@id="pictureurls"]//img/@src').extract()]
            item['domain'] = 'http://www.xgmm.cc/'
            item['page'] = response.url
            log.msg('fetch %d images from %s' % (len(item['urls']), response.url), level='INFO')
            yield item