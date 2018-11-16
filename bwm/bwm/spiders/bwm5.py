# -*- coding: utf-8 -*-
import scrapy
from bwm.items import BwmItem

class Bwm5Spider(scrapy.Spider):
    name = 'bwm5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    def parse(self, response):
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # print(urls)

            # for url in urls:
            #     # url = "https:"+url
            #     url= response.urljoin(url)
            urls = list(map(lambda url:response.urljoin(url),urls))
            # print(url)
            item = BwmItem(category=category,urls=urls)
            yield item