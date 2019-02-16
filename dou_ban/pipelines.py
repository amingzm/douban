# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
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
                  value ('%s', '%s', '%s', '%f', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" %
                (item['name'],
                 item['also_known'],
                 item['movie_info'],
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
            raise e
        return item

    # 结束返回运行时间，并格式化起始和终止时间
    def spider_opened(self, spider):
        self.start = time.time()
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start))  # 转化格式
        self.stats.set_value('start_time', start_time, spider=spider)

    def spider_closed(self, spider, reason):
        self.end = time.time()
        finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.end))  # 转化格式
        self.stats.set_value('finish_time', finish_time, spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)

        # 这是计算此时运行耗费多长时间，特意转化为 时:分:秒
        Total_time = self.end - self.start
        m, s = divmod(Total_time, 60)
        h, m = divmod(m, 60)
        self.stats.set_value('Total_time', "共耗时===>%d时:%02d分:%02d秒" % (h, m, s), spider=spider)