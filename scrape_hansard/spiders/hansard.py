import scrapy
import re
import urllib
from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = 'hansard'
    start_urls = ['http://parlinfo.aph.gov.au/parlInfo/search/summary/summary.w3p;adv=yes;orderBy=customrank;page=0;query=Dataset%3Ahansards,hansards80%20Title%3A%22Start%20of%20Business%22;resCount=Default']

    found_urls = set()

    
    def parse(self,response):
        for i in response.css('ul.search-filter-results').css('.action > a::attr(href)'):
            new_url = i.extract()
            if re.match('^.*xml$',new_url):
                if new_url not in self.found_urls:
                    data = urllib.request.urlopen(new_url).read().decode('utf-8')
                    parsed_data = BeautifulSoup(data,'xml')
                    chamber = BeautifulSoup(data,'xml').find('chamber').get_text()
                    if chamber=='House of Reps':
                        chamber = 'HoR'
                    filename = './data/'+parsed_data.find('date').contents[0] +'-' + chamber + '.xml'
                    with open(filename,'w+') as f:
                        f.write(data)
                    self.found_urls.add(new_url)
        next_page_url = response.css('.results-pagination').css('ul').css('li.next > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url = next_page_url,callback = self.parse)
