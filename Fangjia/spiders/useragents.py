# -*- coding: utf-8 -*

import scrapy
from ..items import UserAgentsItem, PorxyItem
from scrapy.loader import ItemLoader
import re


class UserAgentSpider(scrapy.Spider):
    name = "useragent"
    start_urls = (
        'http://www.useragentstring.com/pages/useragentstring.php',
    )

    def parse(self, response):
        urls = response.xpath(
            "//table[@id='auswahl']/tr[1]/td[2]/a[@class='unterMenuName']/@href").extract()
        for url in urls:
            u = "http://www.useragentstring.com" + url
            yield scrapy.Request(url=u.strip(), callback=self.go_to_page)

    def go_to_page(self, response):
        strings = response.xpath('//*[@id="liste"]/ul/li/a/text()').extract()
        items = []
        for string in strings:
            item = UserAgentsItem()
            item['name'] = string
            items.append(item)
        return items


class XiciSpider(scrapy.Spider):
    name = "xici"
    start_urls = (
        'http://www.xicidaili.com/nt/1',
        'http://www.xicidaili.com/nt/2',
    )

    def parse(self, response):
        table = response.xpath('//table[@id="ip_list"]')
        trs = table[0].xpath('tr')
        items = []
        for tr in trs[1:]:
            item = PorxyItem()
            item['ip'] = tr.xpath('td[2]/text()')[0].extract()
            item['port'] = tr.xpath('td[3]/text()')[0].extract()
            item['position'] = tr.xpath('string(td[4])')[0].extract().strip()
            item['http_type'] = tr.xpath('td[6]/text()')[0].extract()
            item['speed'] = tr.xpath(
                'td[7]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            item['connect_time'] = tr.xpath(
                'td[8]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            item['check_time'] = tr.xpath('td[10]/text()')[0].extract()
            items.append(item)
        return items


class TestProxySpider(scrapy.Spider):
    name = 'testproxy'
    start_urls = []
    for i in range(10):
        start_urls.append('http://ip.filefab.com/index.php')

    def parse(self, response):
        l = ItemLoader(item=UserAgentsItem(), response=response)
        l.add_xpath('name', '//*[@id="ipd"]/span/text()')
        return l.load_item()


class HideMyAssProxySpider(scrapy.Spider):
    name = 'hideproxy'
    start_urls = ['http://proxylist.hidemyass.com/search-1736953']

    def parse(self, response):
        lines = response.css('html').extract()[0]
        bad_class_list = re.findall(
            '\.([a-zA-Z0-9_\-]{4})\{display:none\}', lines)
        bad_class = '(' + '|'.join(bad_class_list) + ')'

        to_remove = '(<span class\="' + bad_class + \
            '">[0-9]{1,3}</span>|<span style=\"display:(none|inline)\">[0-9]{1,3}</span>|<div style="display:none">[0-9]{1,3}</div>|<span class="[a-zA-Z0-9_\-]{1,4}">|</?span>|<span style="display: inline">)'

        junk = re.compile(to_remove, flags=re.M)
        junk = junk.sub('', lines)
        junk = junk.replace("\n", "")

        proxy_src = re.findall(
            '([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s*</td>\s*<td>\s*([0-9]{2,6}).{100,1200}(socks4/5|HTTPS?)', junk)

        list = ''
        items = []
        for src in proxy_src:
            if src:
                item = PorxyItem()
                item['ip'] = src[0]
                item['port'] = src[1]
                if src[2] == 'socks4/5':
                    item['http_type'] = 'socks5h'
                else:
                    item['http_type'] = src[2].lower()
                items.append(item)
        return items
