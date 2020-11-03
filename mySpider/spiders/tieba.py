import re
import json
import time
import scrapy
from . import helper
from scrapy.http import Request
from mySpider.items import MyspiderItem

class Myspider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['baidu.com']
    # baseurl_to_pages = {'https://tieba.baidu.com/f/search/res?isnew=1&kw=%D2%BB%C4%A8%D7%D4%B2%D0%B5%C4%D0%A6&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 5,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%B2%D0%B7%C7%B2%A1&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 1,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%D1%AA&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 6,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%D2%D6%D3%F4&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 20,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%D2%D6%D3%F4%D6%A2&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 76,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%BE%AB%C9%F1%B2%A1&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 3,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%D0%C4%C0%ED%D1%A7&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 15,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%CB%AB%CF%E0%C7%E9%B8%D0%D5%CF%B0%AD&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 1,
    #                     'https://tieba.baidu.com/f/search/res?isnew=1&kw=%C9%A5&qw=%D7%D4%B2%D0&un=&rn=10&sd=&ed=&sm=1&only_thread=1': 7}
    baseurl_to_pages = {"https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%D7%D4%B2%D0&rn=10&un=&only_thread=1&sm=1&sd=&ed=": 76,
                        "https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%D7%D4%CE%D2%C9%CB%BA%A6&rn=10&un=&only_thread=1&sm=1&sd=&ed=": 38}
    currenturl = ''

    def start_requests(self):
        for baseurl, pages in self.baseurl_to_pages.items():
            for i in range (pages):
                url = baseurl + "&pn=" + str(i+1)
                time.sleep(1)
                yield Request(url, self.parse)

    def parse(self, response):
        sel = scrapy.Selector(response)
        posts = sel.xpath('//div[@class="s_post"]')
        for post in posts:
            link = post.xpath('./span/a/@href').extract_first()
            self.currenturl = "https://tieba.baidu.com" + link
            time.sleep(1)
            yield Request(self.currenturl, self.detail_page_parse)

    def detail_page_parse(self, response):
        meta = response.meta
        print("metadata: [" + str(meta) + "]")
        for floor in response.xpath("//div[contains(@class, 'l_post')]"):
            if not helper.is_ad(floor):
                data = json.loads(floor.xpath("@data-field").extract_first())
                print("data: [" + str(data) + "]")
                item = MyspiderItem()
                item['url'] = self.currenturl
                content = floor.xpath(".//div[contains(@class,'j_d_post_content')]/text()").extract_first()
                print("content: [" + str(helper.strip_blank(content)) + "]")
                item['content'] = helper.strip_blank(content)
                if 'date' in data['content'].keys():
                    timestamp = data['content']['date']
                else:
                    timestamp = floor.xpath(".//span[@class='tail-info']")\
                        .re_first(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
                print("timestamp: [" + str(timestamp) + "]")
                item['timestamp'] = timestamp
                yield item

            time.sleep(1)