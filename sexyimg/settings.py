# Scrapy settings for sexyimg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sexyimg'

SPIDER_MODULES = ['sexyimg.spiders']
NEWSPIDER_MODULE = 'sexyimg.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'sexyimg (+http://www.yourdomain.com)'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'sexyimg.pipelines.SexyimgPipeline': 300
}

LOG_FILE = 'scrapy.log'
LOG_LEVEL = 'INFO'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'sexyimg.rotate_useragent.RotateUserAgentMiddleware': 400
}