# -*- coding: utf-8 -*-
import urllib
import re

from datetime import datetime

import scrapy
from work.items import WorkItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

vacancy_count_re = re.compile(r'(\d+)')

class WorkSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ua"]
    start_urls = [
        "http://www.hh.ua/"
    ]

    def __init__(self, searchterm='', *args, **kwargs):
        self.searchterm = searchterm
        super(WorkSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['{}search/vacancy?text={}&area=5'.format(self.start_urls[0], searchterm)]

    def parse(self, response):
        vacancy_count = response.xpath("//*[@class='resumesearch__result-count']/text()").extract()
        pages = 0
        if vacancy_count:
            vacancy_count = vacancy_count[0]
            pages = int(''.join(vacancy_count_re.findall(vacancy_count))) / 20
        for i in range(pages + 1):
            url = '{}&page={}'.format(self.start_urls[0], i)
            yield scrapy.Request(url, callback=self.parse_contents)



    def parse_contents(self, response):
        # page = response_url_re.findall(response._url)[0]
        elements = response.xpath("//*[@class='search-result']/div")

        for element in elements:
            work_item = WorkItem()
            work_item['vacancy'] = element.xpath('div/div/div/a/text()').extract()[0].strip()
            work_item['link'] = element.xpath('div/div/div/a/@href').extract()[0].strip()
            work_item['salary'] = ''
            salary = element.xpath("div/div/div[@class='b-vacancy-list-salary']/text()").extract()
            if salary:
                work_item['salary'] = salary[0].strip()
            yield work_item