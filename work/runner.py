# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from work import settings

def run_spiders():
    process = CrawlerProcess(get_project_settings())
    for spider in settings.SPIDERS:
        process.crawl(spider, searchterm='программист')
    process.start()
    print 'finished'

if __name__ == "__main__":
    run_spiders()