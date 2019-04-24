import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "promedGetData"

    def start_requests(self):
        urls = []
        with open('promed.json') as json_file:
            data = json.load(json_file)
            for p in data:
                temp = p['id'][4:len(p['id'])-2]
                urls.append('http://www.promedmail.org/ajax/getPost.php?alert_id='+temp)
                
        for url in urls:
           yield scrapy.Request(url=url, callback=self.parse, headers={"Referer": "http://www.promedmail.org/post/"+temp})
    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        for quote in response.css('a'):
            yield {
                #'id': quote.xpath('@id').get(),
            }