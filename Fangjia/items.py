# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re


class FangjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    acreage = scrapy.Field()
    cityCode = scrapy.Field()
    dealAvgPrice = scrapy.Field()
    districtName = scrapy.Field()
    face = scrapy.Field()
    floor_state = scrapy.Field()
    hall = scrapy.Field()
    houseSellId = scrapy.Field()
    isAutoTitle = scrapy.Field()
    isRecommend = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    mainPhotoUrl = scrapy.Field()
    metroRemark = scrapy.Field()
    plateName = scrapy.Field()
    propertyName = scrapy.Field()
    propertyNo = scrapy.Field()
    referAvgPrice = scrapy.Field()
    room = scrapy.Field()
    showPrice = scrapy.Field()
    tags = scrapy.Field()
    title = scrapy.Field()
    unitPrice = scrapy.Field()
    videoDisplay = scrapy.Field()


class XiaoquItem(scrapy.Item):

    def get_latitude(source):
        listdata = re.findall('[0-9]*\.?[0-9]+',source[0])
        return [listdata[1]]

    def get_longitude(source):
        listdata = re.findall('[0-9]*\.?[0-9]+',source[0])
        return [listdata[0]]
    
    def get_build_year(source):
        source[0]=re.sub(u'(\\n|\\t|\ |年)','',source[0])
        return source

    def remove_useless_tag(source):
        result=''
        for item in source:
            result+=re.sub('(\\t\\n|\\n|\\t|\ )','',item)
        return [result]

    xid = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field(output_processor=get_latitude)
    longitude = scrapy.Field(output_processor=get_longitude)
    avgPrice = scrapy.Field()
    buildYear = scrapy.Field(output_processor=get_build_year)
    propertyName = scrapy.Field(output_processor=remove_useless_tag)
    propertyPrice = scrapy.Field(output_processor=remove_useless_tag)
    region = scrapy.Field(output_processor=remove_useless_tag)
    developer = scrapy.Field(output_processor=remove_useless_tag)
    ringLine = scrapy.Field(output_processor=remove_useless_tag)

class UserAgentsItem(scrapy.Item):
    name = scrapy.Field()


class PorxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    position = scrapy.Field()
    http_type = scrapy.Field()
    speed = scrapy.Field()
    connect_time = scrapy.Field()
    check_time = scrapy.Field()