# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 15:29
# @Author  : Ming
import json

import scrapy

from dou_ban.items import DoubanItem

from scrapy import Selector


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ['https://movie.douban.com/subject/26588308/']

    def parse(self, response):
        item = DoubanItem()
        selector = Selector(response)
        one_movie = selector.xpath('//div[@id="content"]')
        text = one_movie.xpath('string(.//div[@id="info"])')  # 提取标签内的文本

        item['score'] = one_movie.xpath('.//strong[@class="ll rating_num"]/text()').extract()
        # 从script中获取其余的值
        json_data = json.loads(selector.xpath('//script[@type="application/ld+json"]/text()').extract()[0].replace('\n', ''))
        item['name'] = json_data.get('name')
        item['also_known'] = one_movie.xpath('.//div[@id="info"]/span[last() - 2]/text()').extract()[0]
        item['movie_info'] = json_data.get('description')
        item['score'] = json_data.get('aggregateRating').get('ratingValue')

        item['director'] = self.json_util(json_data.get('director'))
        item['screenwriter'] = self.json_util(json_data.get('author'))
        item['stars'] = self.json_util(json_data.get('actor'))
        item['genre'] = ''.join([e for e in one_movie.xpath('.//span[@property="v:genre"]/text()').extract()])
        item['country'] = text.re(r'地区:(.*)\n')[0]
        item['language'] = text.re(r'语言:(.*)\n')[0]
        item['release_date'] = json_data.get('datePublished')
        item['runtime'] = text.re(r'片长:(.*)\n')[0]
        # print(json.loads(json_data[0]).get('director'))
        # print(len(json_data))
        yield(item)

    # 提取json中的name，并拼接字符串返回
    def json_util(self, json_data):
        result = ''
        for temp in json_data:
            result = result + temp.get('name') + '/'
        return result.rstrip('/')
