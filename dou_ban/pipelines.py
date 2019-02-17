# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import time

import pymysql

from dou_ban import settings


class DouBanPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into movie(name, also_known, movie_info, score, director, screenwriter, stars, genre, country, language, release_date, runtime, url) 
                  value ('%s', '%s', '%s', '%f', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" %
                (self.escape_string(item['name']),
                 self.escape_string(item['also_known']),
                 self.escape_string(item['movie_info']),
                 float(item['score']),
                 item['director'],
                 item['screenwriter'],
                 item['stars'],
                 item['genre'],
                 item['country'],
                 item['language'],
                 item['release_date'],
                 item['runtime'],
                 item['url'])
            )  # 要用%不能用逗号，不然float赋值失败
            self.connect.commit()
        except Exception as e:
            logging.error(e)
            raise e
        return item

    def escape_string(self, s):
        return s.replace("'", "\\'")