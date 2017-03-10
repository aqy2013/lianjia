# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64
import json
import logging
import random

from scrapy import signals

log = logging.getLogger('scrapy.proxies')


class FangjiaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        f = open("useragents.json")
        setting = json.load(f)
        return cls(setting)

    def process_start_requests(self, request, spider):
        for req in request:
            if spider.name == 'xiaoqu':
                yield req
            else:
                useragent = random.choice(self.agents)['name']
                log.debug('User-Agent:%s' % useragent)
                req.headers.setdefault('User-Agent', useragent)
                yield req


class ProxyMiddleware(object):

    def __init__(self, proxies):
        self.proxies = proxies
        self.index = 0
        self.chosen_proxy = None

    @classmethod
    def from_crawler(cls, crawler):
        f = open("proxylist.json")
        proxies = json.load(f)
        return cls(proxies)
        # return cls(crawler.settings.getlist('PROXY_LIST'))

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        proxy = request.meta['proxy']
        try:
            del self.proxies[proxy]
        except KeyError:
            pass
        request.meta["exception"] = True
        self.chosen_proxy = random.choice(self.proxies)

        proxy = '%s://%s:%s' % (self.chosen_proxy['http_type'],
                                self.chosen_proxy['ip'], self.chosen_proxy['port'])
        log.debug('Chose Proxy:%s, %s proxies left' %
                  (proxy, len(self.proxies)))

    def process_start_requests(self, request, spider):
        self.chosen_proxy = random.choice(self.proxies)
        for req in request:
            if spider.name == 'hideproxy':
                yield req
            else:
                if self.index % 50 == 0:
                    self.chosen_proxy = random.choice(self.proxies)
                self.index = self.index + 1
                proxy = '%s://%s:%s' % (self.chosen_proxy['http_type'],
                                        self.chosen_proxy['ip'], self.chosen_proxy['port'])
                log.debug('Proxy:%s' % proxy)
                req.meta['proxy'] = proxy
                yield req
