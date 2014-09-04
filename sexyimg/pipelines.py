# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import datetime


class SexyimgPipeline(object):
    def __init__(self):
        now = datetime.datetime.now()
        self.file = codecs.open('img_data_%s.json' % now.strftime('%Y%m%d%H%M%S'), mode='wb', encoding='utf-8')
        pass

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode('unicode_escape'))
        return item

    def __del__(self):
        self.file.close()