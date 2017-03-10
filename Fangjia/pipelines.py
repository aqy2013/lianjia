# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request


class FangjiaPipeline(object):
    collection_name = 'price_items'

    def __init__(self):
        self.conn = MySQLdb.connect(
            user='root', passwd='password', db='test', host='localhost', charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == 'xiaoqu':
            try:
                price = item['avgPrice']
                print('Price : %s', price)

                self.cursor.execute("""INSERT INTO fangjia (
                    xid,
                    title,
                    avgPrice,
                    latitude,
                    longitude,
                    buildyear,
                    address,
                    propertyName,
                    propertyPrice,
                    region,
                    developer,
                    ringLine
                    ) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                    (
                                        item['xid'],
                                        item['title'],
                                        price,
                                        item['latitude'],
                                        item['longitude'],
                                        item['buildYear'],
                                        item['address'],
                                        item['propertyName'],
                                        item['propertyPrice'],
                                        item['region'],
                                        item['developer'],
                                        item['ringLine'],
                                    ))
                self.conn.commit()
                return item
            except Exception, e:
                print "DB Error %s" % (e)
                DropItem(item)
        else:
            return item
