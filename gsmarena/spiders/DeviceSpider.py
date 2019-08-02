# -*- coding: utf-8 -*-
import scrapy


class DevicespiderSpider(scrapy.Spider):
    name = 'DeviceSpider'
    allowed_domains = ['www.gsmarena.com/makers.php3']
    start_urls = ['http://www.gsmarena.com/makers.php3/']

    def parse(self, response):
        print("hello!")
        brands = response.css(".st-text a")
        for brand in brands:
            brandname = brand.css("a::text").extract()
            brandurl = brand.css("a::attr(href)").extract()
            print(brandname[0] + "->" + brandurl[0])
