# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import csv

class MyspiderPipeline:
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/tieba.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'a+', encoding="utf-8", newline='')
        # csv写法
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        if item['content']:
            self.writer.writerow([item['url'], item['content'], item['timestamp']])
        return item

    def close_spider(self, spider):
        self.file.close()