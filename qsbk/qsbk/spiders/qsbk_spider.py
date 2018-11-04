# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
from qsbk.items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'   #　爬虫名字
    allowed_domains = ['qiushibaike.com']  #　限制爬取范围
    start_urls = ['https://www.qiushibaike.com/text/page/1/'] # 爬取开始的页面

    def parse(self, response):
        duanzidivs = response.xpath("//div[@id='content-left']/div")
        for duanzidiv in duanzidivs:
            author = response.xpath(".//h2/text()").get().strip()
            content = response.xpath("//div[@class='content']//text()").getall()  # getall()和extract()用法一样
            content = "".join(content).strip()

            # 把数据传给pipelines
            # duanzi = {"author":author,"content":content}
            # yield duanzi


            # 优化前面的代码，不用字典
            item = QsbkItem(author=author,content=content)
            yield item