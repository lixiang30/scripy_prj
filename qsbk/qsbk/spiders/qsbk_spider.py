# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
from qsbk.items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'   #　爬虫名字
    allowed_domains = ['qiushibaike.com']  #　限制爬取范围
    start_urls = ['https://www.qiushibaike.com/text/page/1/'] # 爬取开始的页面
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        duanzidivs = response.xpath("//div[@id='content-left']/div")
        for duanzidiv in duanzidivs:
            author = duanzidiv.xpath(".//h2/text()").get().strip()
            content = duanzidiv.xpath("//div[@class='content']//text()").getall()  # getall()和extract()用法一样
            content = "".join(content).strip()

            # 把数据传给pipelines
            # duanzi = {"author":author,"content":content}
            # yield duanzi


            # 优化前面的代码，不用字典
            item = QsbkItem(author=author,content=content)
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)