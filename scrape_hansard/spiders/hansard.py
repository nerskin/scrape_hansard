import scrapy
import re
import urllib

class QuotesSpider(scrapy.Spider):
    name = 'hansard'
    start_urls = ['https://www.aph.gov.au/Parliamentary_Business/Hansard/Search?__VIEWSTATEGENERATOR=20B6B7A5&ind=0&st=1&sr=0&q=&hto=1&expand=False&drvH=0&pnuH=0&f=01%2F01%2F2018&to=17%2F08%2F2018&pi=0&pv=&chi=0&coi=0&ps=100']

    found_urls = set()

    def parse(self, response):
        for i in response.css('ul.search-filter-results').css('.action > a::attr(href)'):
            new_url = i.extract()
            if re.match('^.*xml$',new_url):
                if new_url not in self.found_urls:
                    data = urllib.request.urlopen(new_url).read().decode('utf-8')
                    with open('hansard.xml','a+') as f:
                        f.write(data)
                    self.found_urls.add(new_url)
        next_page_url = response.css('.results-pagination').css('ul').css('li.next > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url = next_page_url,callback = self.parse)
