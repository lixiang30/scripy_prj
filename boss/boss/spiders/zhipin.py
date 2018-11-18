# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boss.items import BossItem


class ZhipingSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/c100010000-p100109/?page=2&ka=page-2']

    rules = (
        # 匹配职位列表页的规则
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d'), follow=True),

        # 匹配职位详情页的规则
        Rule(LinkExtractor(allow=r'.+job_detail/\d+.html'),callback="parse_job",follow=False),
    )

    # def parse_item(self, response):
    #     i = {}
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return i

    def parse_job(self,response):
        name = response.xpath("//div[@class='name']/h1/text()").get().strip()
        salary = response.xpath("//div[@class='name']/span/text()").get().strip()
        city = response.xpath("//div[@class='info-primary']/p/text()").get().strip()
        job_info = response.xpath("//div[contains(@class,'job-primary')]/div[@class='info-primary']/p//text()").getall()
        city = job_info[0]
        work_years = job_info[1]
        education = job_info[2]
        company = response.xpath("//a[@ka='job-detail-company']/text()").get()

        item = BossItem(name=name,salary=salary,city=city,work_years=work_years,education=education,company=company)
        yield item


