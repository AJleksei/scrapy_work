# -*- coding: utf-8 -*-

import urllib
import re

from scrapy import Spider, Selector, Request

from work.items import WorkItem

last_page_re = re.compile(r'<a .+>(.+)<\/a>')

class RabotaSpider(Spider):
    name = 'rabota'
    start_urls = [u'http://rabota.ua/jobsearch/vacancy_list']

    def __init__(self, searchterm='', *args, **kwargs):
        self.searchterm = searchterm
        super(RabotaSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['{}?keyWords={}'.format(self.start_urls[0], searchterm)]

    def parse(self, response):
        pages = response.xpath('//tr[@class="vlp"]/td/dl/dd').extract()
        last_page = 0
        if pages:
            last_page = int(last_page_re.findall(pages[-2])[0])
        #last_page = 5
        if last_page:
            for page in range(1, last_page+1):
                url = '{}&pg={}'.format(self.start_urls[0], page)
                yield Request(url, self.parse_page)

    def parse_page(self, response):
        for v in response.xpath('//td/div[1]'):
            item = WorkItem()
            item['vacancy'] = v.xpath('div/h3/a/text()').extract()[0].strip()
            item['link'] = v.xpath('div/h3/a/@href').extract()[0]
            salary = v.xpath('div/div/b/text()').extract()
            if salary:
                item['salary'] = salary[0]
            else:
                item['salary'] = ''

            yield item
