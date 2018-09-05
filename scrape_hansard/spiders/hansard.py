import scrapy
import re
import urllib
from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = 'hansard'
    start_urls = ['https://www.aph.gov.au/Parliamentary_Business/Hansard/Search?__VIEWSTATEGENERATOR=20B6B7A5&ind=0&st=1&sr=0&q=&hto=1&expand=False&drvH=0&drt=2&pnu=45&pnuH=45&f=30%2F08%2F2016&to=18%2F08%2F2018&pi=0&pv=&chi=0&coi=0&ps=100','https://www.aph.gov.au/Parliamentary_Business/Hansard/Search?__VIEWSTATEGENERATOR=20B6B7A5&ind=0&st=1&sr=0&q=&hto=1&expand=False&drvH=0&drt=2&pnu=44&pnuH=44&f=12%2F11%2F2013&to=29%2F08%2F2016&pi=0&pv=&chi=0&coi=0&ps=100']

    found_urls = set()

    
    def parse(self,response):
        for i in response.css('ul.search-filter-results').css('.action > a::attr(href)'):
            new_url = i.extract()
            if re.match('^.*xml$',new_url):
                if new_url not in self.found_urls:
                    data = urllib.request.urlopen(new_url).read().decode('utf-8')
                    parsed_data = BeautifulSoup(data,'xml')
                    chamber = BeautifulSoup(data).find('chamber')
                    filename = './data/'+parsed_data.find('date').contents[0] +'-' + chamber + '-'  + '.xml'
                    with open(filename,'w+') as f:
                        f.write(data)
                    self.found_urls.add(new_url)
        next_page_url = response.css('.results-pagination').css('ul').css('li.next > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url = next_page_url,callback = self.parse)
