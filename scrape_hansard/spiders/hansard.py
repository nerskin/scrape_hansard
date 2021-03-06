import scrapy
import re
import urllib.request
from bs4 import BeautifulSoup
import ssl

class QuotesSpider(scrapy.Spider):
    name = 'hansard'
    start_urls = ['https://www.aph.gov.au/Parliamentary_Business/Hansard/Search?__VIEWSTATEGENERATOR=20B6B7A5&ind=0&st=1&sr=0&q=&hto=1&expand=False&drvH=0&pnuH=0&f=01%2F01%2F2000&to=dd%2Fmm%2Fyyyy&pi=0&pv=&chi=1&ps=100',
                  'https://www.aph.gov.au/Parliamentary_Business/Hansard/Search?__VIEWSTATEGENERATOR=20B6B7A5&ind=0&st=1&sr=0&q=&hto=1&expand=False&drvH=0&pnuH=0&f=2000%2F01%2F01&to=&pi=0&pv=&chi=2&ps=10']
    found_urls = set()

    
    def parse(self,response):
        ssl._create_default_https_context = ssl._create_unverified_context#don't bother with certificates
        for i in response.css('ul.search-filter-results').css('.action > a::attr(href)'):
            new_url = i.extract()
            if re.search('xml$',new_url):
                if new_url not in self.found_urls:
                    data = urllib.request.urlopen(new_url).read().decode('utf-8')
                    print('\a')
                    parsed_data = BeautifulSoup(data,'xml')
                    chamber = BeautifulSoup(data,'xml').find('chamber').get_text()
                    if chamber=='House of Reps':
                        chamber = 'HoR'
                    filename = './data/'+parsed_data.find('date').contents[0] +'-' + chamber + '.xml'
                    with open(filename,'w+') as f:
                        f.write(data)
                        print('\a') 
                        print(filename)
                    self.found_urls.add(new_url)
        next_page_url = response.css('.results-pagination').css('ul').css('li.next > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url = next_page_url,callback = self.parse)
