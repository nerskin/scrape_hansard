# -*- coding: utf-8 -*-
import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = 'hansard' 
    start_urls = ['https://www.aph.gov.au/Parliamentary_Business/Hansard/Search?__VIEWSTATEGENERATOR=20B6B7A5&ind=0&st=1&sr=0&q=&hto=1&expand=False&drvH=7&drt=2&pnu=45&pnuH=45&f=30%2F08%2F2016&to=16%2F08%2F2018&pi=0&pv=&chi=0&coi=0&ps=100']

    def parse(self, response):
        with open('log.txt','a') as f:
            f.write(response.url)
        for i in response.css('ul.search-filter-results').css('.action > a::attr(href)'):
            if re.match('.*xml$',i.extract()):
                yield {'url' : i.extract()}
        next_page_url = response.css('.results-pagination').css('ul').css('li.next > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url = next_page_url,callback = self.parse)
