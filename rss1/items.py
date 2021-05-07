# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Rss1Item(scrapy.Item):
    # define the fields for your item here like:
    index = scrapy.Field()
    description = scrapy.Field()
    pubDate = scrapy.Field()
    link = scrapy.Field()
    crawl_url = scrapy.Field()
    pass
