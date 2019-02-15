# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    name = scrapy.Field()
    also_known = scrapy.Field()
    movie_info = scrapy.Field()
    score = scrapy.Field()

    director = scrapy.Field()
    screenwriter = scrapy.Field()
    stars = scrapy.Field()
    genre = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    release_date = scrapy.Field()
    runtime = scrapy.Field()
    # color = scrapy.Field()
