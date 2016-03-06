# -*- coding: utf-8 -*-
import urllib
import re

from datetime import datetime

import scrapy
from work.items import WorkItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

response_url_re = re.compile(r'page=(\d+)')

class WorkSpider(scrapy.Spider):
    name = "work"
    allowed_domains = ["work.ua"]
    start_urls = [
        "http://www.work.ua/"
    ]

    def __init__(self, searchterm='', *args, **kwargs):
        self.searchterm = searchterm
        super(WorkSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['{}jobs-{}/'.format(self.start_urls[0], searchterm)]

    """
    def start_requests(self):
        self.start_urls[0] = '{}{}/?days=125&page=1'\
            .format(self.start_urls, urllib.quote_plus(self.urls))
        yield self.make_requests_from_url(self.start_urls[0])
    """
    def parse(self, response):
        pages = response.xpath('//*[@id="center"]/div/div/div/nav/ul/li[last()-1]/a/text()').extract()
        if pages:
            pages = int(pages[0])
        pages = 5
        for i in range(1, pages):
            url = '{}?days=125&page={}'.format(self.start_urls[0], i)
            yield scrapy.Request(url, callback=self.parse_contents)

    def parse_contents(self, response):
        # page = response_url_re.findall(response._url)[0]
        elements = response.css('#center > div > div.row > '
                                'div.col-md-8.col-left > div.card-hover')

        for element in elements:
            work_item = WorkItem()
            work_item['vacancy'] = element.xpath('h2/a/text()').extract()[0].strip()
            work_item['link'] = element.xpath('h2/a/@href').extract()[0].strip()
            work_item['salary'] = ''
            salary = element.xpath('h2/span/span[2]/text()').extract()
            if salary:
                work_item['salary'] = salary[0].strip()
            print u'{} - {}'.format(work_item['salary'], work_item['vacancy'])
            yield work_item


        """
        filename = 'test.txt'
        with open(filename, 'a') as f:
            f.write(res_all)
        """
        # work_item = WorkItem()
        # work_item.vacancy = response.xpath('//*[@id="center"]/div/div/div/nav/ul/li[last()-1]/a/text()').extract()


        """
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        """

    """
    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item


    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
            """


"""
    def parse_articles_follow_next_page(self, response):
        for article in response.xpath("//article"):
            item = ArticleItem()

            ... extract article data here

            yield item

        next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_articles_follow_next_page)
"""
