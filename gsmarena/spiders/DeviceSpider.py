# -*- coding: utf-8 -*-
import scrapy
import json


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
                request = scrapy.Request(brand_page, meta={'brand': brandname[0]}, callback=self.devicelistparse)
                yield request
            break

    def devicelistparse(self, response):
        devicelist = response.css("div.makers a")
        brand = response.meta['brand']
        # print(brand)
        for device in devicelist:
            device_page = device.css("a::attr(href)").extract()
            device_page = response.urljoin(device_page[0])
            # print(device_page)
            yield scrapy.Request(device_page, meta={'brand': brand}, callback=self.deviceParse)
        next_page = response.css("a.pages-next ::attr(href)").extract()
        if next_page:
            next_page = response.urljoin(next_page[0])
            yield scrapy.Request(next_page, meta={'brand': brand}, callback=self.deviceListParse)

    def deviceParse(self, response):
        global date
        date = {}
        deviceInfo = response.css("div#specs-list table")
        deviceName = response.css("h1.specs-phone-name-title ::text").extract()
        brand = response.meta['brand']
#        date = {'brand': brand, 'deviceNo': deviceName[0]}
        date['brand'] = brand
        if deviceName:
            date['deviceNo'] = deviceName[0]
        for table in deviceInfo:
            tit = table.css("th::text").extract()
            date[tit[0]] = {}
            trs = table.css("tr")
            for tr in trs:
                attr = tr.css("td.ttl a ::text").extract()
                nfo = tr.css("td.nfo a ::text").extract()
                if not nfo:
                    nfo = tr.css("td.nfo ::text").extract()
                if attr:
                    if nfo:
                        date[tit[0]][attr[0]] = nfo[0]
                    else:
                        date[tit[0]][attr[0]] = ""
                elif nfo:
                    date[tit[0]][nfo[0]] = nfo[0]

        fo = open("Info/" + brand + ".json", "a")
        json.dump(date, fo)
        fo.close()
