# coding:utf-8
from itertools import product
from ..items import FangjiaItem, XiaoquItem
import scrapy
import re
from scrapy.loader import ItemLoader
import MySQLdb


class HousePriceSpider(scrapy.Spider):

    def parse(self, response):
        item_list = response.css(
            '#house-lst a[name=selectDetail]::attr(href)').extract()
        for item in item_list:
            yield scrapy.Request(self.base_url + item, callback=self.parse_detail)

        # next_page_url = response.css(
        #     '.house-lst-page-box a[gahref=results_next_page]').xpath('href()').extract_first()
        # if next_page_url is not None:
        #     # 递归下一页
        # yield scrapy.Request(response.urljoin(next_page_url),
        # callback=self.parse)

    def parse_detail(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        title = response.css('.content .title h1.main::text').extract()
        price = FangjiaItem()
        price['title'] = title
        return price
        # 如果下一页，则回调循环

    name = 'price'
    base_url = 'http://sh.lianjia.com'
    start_urls = []
    # 可筛选条件
    districts = {
        'pudongxinqu': '浦东',
        'minhang': '闵行',
        'baoshan': '宝山',
        'xuhui': '徐汇',
        'putuo': '普陀',
        'yangpu': '杨浦',
        'changning': '长宁',
        'songjiang': '松江',
        'jiading': '嘉定',
        'huangpu': '黄浦',
        'jingan': '静安',
        'zhabei': '闸北',
        'hongkou': '虹口',
        'qingpu': '青浦',
        'fengxian': '奉贤',
        'jinshan': '金山',
        'chongming': '崇明'
    }
    prices = {
        'p21': '200万以下',
        'p22': '200-300万',
        'p23': '300-400万',
        'p24': '400-500万',
        'p25': '500-800万',
        'p26': '800-1000万',
        'p27': '1000万以上',
    }
    areas = {
        'a1': '50平以下',
        'a2': '50-70平',
        'a3': '70-90平',
        'a4': '90-110平',
        'a5': '110-130平',
        'a6': '130-150平',
        'a7': '150平以上',
    }
    rooms = {'l1': '一室', 'l2': '二室', 'l3': '三室',
             'l4': '四室', 'l5': '五室', 'l6': '五室以上', }
    faces = {'f1': '东', 'f2': '南', 'f3': '西', 'f4': '北', 'f10': '南北', }
    house_ages = {'y1': '2年内', 'y2': '2-5年',
                  'y3': '5-10年', 'y4': '10-20年', 'y5': '20年以上', }
    floors = {'c1': '低区', 'c2': '中区', 'c3': '高区', }
    decorations = {'x1': '精装', 'x2': '豪装',
                   'x3': '中装', 'x4': '简装', 'x5': '毛坯', }
    house_type_codes = {'o1': '公寓', 'o2': '商住', 'o3': '别墅', 'o4': '其他', }

    # type_keys = product(prices.keys(), areas.keys(), rooms.keys(), faces.keys(
    # ), house_ages.keys(), floors.keys(), decorations.keys(), decorations.keys(), house_type_codes.keys())

    type_keys = product(prices.keys(), areas.keys())
    start_urls = [base_url + '/ershoufang/']
    # 排列组合所有条件
    # list_urls = {}
    # for district in districts:
    #     for type_key in type_keys:
    #         url = base_url + '/ershoufang/' + district + '/' + ''.join(type_key)
    #         list_urls[url] = 0
    #         start_urls.append(url)


# 爬取小区
class XiaoquSpider(scrapy.Spider):
    name = 'xiaoqu'
    allowed_domains = ["lianjia.com"]
    base_url = 'http://sh.lianjia.com'
    start_urls = [base_url + '/xiaoqu/']

    def __init__(self):
        conn = MySQLdb.connect(
            user='root', passwd='password', db='test', host='localhost', charset="utf8")
        cursor = conn.cursor()
        cursor.execute('select distinct(xid) from fangjia')
        result = cursor.fetchall()
        self.cids = []
        for item in result:
            self.cids.append(item[0])

    def parse(self, response):
        # if response.css('#house-lst').extract_first() is None:
        #     yield scrapy.Request(url=response.url, dont_filter=True)
        next_page_url = response.css(
            '.house-lst-page-box a[gahref=results_next_page]::attr(href)').extract_first()
        if next_page_url is not None:
            # 递归下一页
            print u'\r\n※ ※ ※ ※ ※    next page : %s    ※ ※ ※ ※ ※\r\n' % next_page_url
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

        item_list = response.css(
            '#house-lst a[name=selectDetail]::attr(href)').extract()
        print u'※ ※ ※ ※ ※    current total : %d    ※ ※ ※ ※ ※' % len(item_list)
        for item in item_list:
            cid = re.search(r'\d{1,}', item).group()
            if cid in self.cids:
                # print u'※ ※ ※ ※ ※    skip : %s    ※ ※ ※ ※ ※' % cid
                pass
            else:
                yield scrapy.Request(self.base_url + item, callback=self.parse_detail)

    def parse_detail(self, response):
        l = ItemLoader(item=XiaoquItem(), response=response)
        xid = re.search('\d{1,}', response.url).group()
        l.add_value('xid', xid)
        l.add_css(
            'title', '.detail-container .detail-block .res-top .title h1::text')
        if response.css('.detail-container .detail-block .top-detail .res-info .priceInfo .p_nodata').extract_first() is None:
            l.add_css(
                'avgPrice', '.detail-container .detail-block .top-detail .res-info .priceInfo .item .p::text', re='\d{1,}')
        # else:
        #     l.add_value('avgPrice', None)
        l.add_css('latitude', '#actshowMap_xiaoqu::attr(xiaoqu)')
        l.add_css('longitude', '#actshowMap_xiaoqu::attr(xiaoqu)')
        l.add_css(
            'buildYear', '#zoneView > div.res-info.fr > div.col-2.clearfix > ol > li:nth-child(2) > span > span::text')
        l.add_css(
            'propertyName', '#zoneView > div.res-info.fr > div.col-2.clearfix > ol > li:nth-child(5) > span::text')
        l.add_css(
            'region', '#zoneView > div.res-info.fr > div.col-2.clearfix > ol > li:nth-child(6) > span::text')
        l.add_css(
            'developer', '#zoneView > div.res-info.fr > div.col-2.clearfix > ol > li:nth-child(5) > span::text')
        l.add_css('propertyPrice',
                  '#zoneView > div.res-info.fr > div.col-2.clearfix > ol > li:nth-child(3) > span::text')
        l.add_css('address', 'div.nav-container.detail-container > section > div.res-top.clear > div.title.fl > span > span.adr::attr(title)')
        l.add_css(
            'ringLine', '#zoneView > div.res-info.fr > div.col-2.clearfix > ol > li:nth-child(7) > span::text')
        print u'※ ※ ※ ※ ※    done : %s    ※ ※ ※ ※ ※' % xid
        return l.load_item()
