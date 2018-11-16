# -*- coding: utf-8 -*-
import scrapy


class Bwm5Spider(scrapy.Spider):
    name = 'bwm5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['http://car.autohome.com.cn/']

    def parse(self, response):
        pass
