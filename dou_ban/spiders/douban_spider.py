# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 15:29
# @Author  : Ming
import json
import re
import time

import scrapy

from dou_ban.items import DoubanItem

from scrapy import Selector, Request


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ['https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0&year_range=2018,2018']
    base_url_prefix = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start='
    base_url_suffix = '&year_range=2018,2018'

    def parse(self, response):
        urls = []
        start = re.search(r'start=(\d*)', response.url).group(1)
        rs = json.loads(response.text)
        test = 0
        data = rs.get('data')
        if len(data) != 0 and test < 1:
            test += 1
            yield Request(self.base_url_prefix + str(int(start) + 20) + self.base_url_suffix, callback=self.parse)
        for temp in data:
            urls.append(temp.get('url'))
        for url in urls:
            yield Request(url, callback=self.parse_item)
        # pass

    def parse_item(self, response):
        item = DoubanItem()
        selector = Selector(response)
        one_movie = selector.xpath('//div[@id="content"]')
        text = one_movie.xpath('string(.//div[@id="info"])')  # 提取标签内的文本

        # item['score'] = one_movie.xpath('.//strong[@class="ll rating_num"]/text()').extract()
        # 从script中获取其余的值
        json_data = json.loads(selector.xpath('//script[@type="application/ld+json"]/text()').extract()[0].replace('\n', ''))
        item['url'] = str(response.url)
        item['name'] = json_data.get('name')
        item['also_known'] = text.re(r'又名:(.*)\n')[0]
        item['movie_info'] = json_data.get('description')
        score = json_data.get('aggregateRating').get('ratingValue')
        if score == '':
            item['score'] = 0.0
        else:
            item['score'] = float(score)

        item['director'] = text.re(r'导演:(.*)\n')[0]
        item['screenwriter'] = text.re(r'编剧:(.*)\n')[0]
        # item['stars'] = self.json_util(json_data.get('actor'))
        item['stars'] = text.re(r'主演:(.*)\n')[0]
        # item['genre'] = ''.join([e for e in one_movie.xpath('.//span[@property="v:genre"]/text()').extract()])
        item['genre'] = text.re(r'类型:(.*)\n')[0]
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


