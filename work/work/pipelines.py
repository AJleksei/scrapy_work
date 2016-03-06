# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv
from work import settings


class WriteToCsv(object):

    def file_name(self, spider):
        return '{}_{}.csv'.format(spider.name, spider.searchterm)

    def write_to_csv(self, item, spider):
        writer = csv.writer(open(self.file_name(spider), 'a'))
        writer.writerow([item[key].encode('utf-8') for key in item.keys()])

    def open_spider(self, spider):
        self.clean_file(spider)

    def process_item(self, item, spider):
        self.write_to_csv(item, spider)
        return item

    def clean_file(self, spider):
        try:
            os.remove(self.file_name(spider))
        except OSError:
            pass


class CsvPipeline(WriteToCsv):
    pass