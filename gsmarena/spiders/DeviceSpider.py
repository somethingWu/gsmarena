# -*- coding: utf-8 -*-
import scrapy


class DevicespiderSpider(scrapy.Spider):
    name = 'DeviceSpider'
    allowed_domains = ['www.gsmarena.com']
    start_urls = ['http://www.gsmarena.com/makers.php3/']

    def parse(self, response):
        brands = response.css(".st-text a")
        for brand in brands:
            brandname = brand.css("a::text").extract()
            brand_page = brand.css("a::attr(href)").extract()
            if brand_page is not None:
                brand_page = response.url.replace("makers.php3/", brand_page[0])
                request = scrapy.Request(brand_page, meta={'brand': brandname[0]}, callback=self.deviceListParse)
                yield request
                break

    def deviceListParse(self, response):
        devicelist = response.css("div.makers a")
        brand = response.meta['brand']
        #print(brand)
        for device in devicelist:
            device_page = device.css("a::attr(href)").extract()
            device_page = response.urljoin(device_page[0])
            #print(device_page)
            yield scrapy.Request(device_page, meta={'brand': brand}, callback=self.deviceParse)
            break

    def deviceParse(self, response):
        deviceInfo = response.css("div#specs-list table")
        deviceName = response.css("h1.specs-phone-name-title ::text").extract()
        brand = response.meta['brand']
        date = {'brand' : brand, 'deviceNo' : deviceName}
        for table in deviceInfo:
            tit = table.css("th::text").extract()
            date[tit[0]] = {}
            print(deviceName)
            print(table.css("*").extract())
            break
