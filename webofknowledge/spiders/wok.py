# -*- coding: utf-8 -*-
import scrapy
import requests

from webofknowledge.items import WebofknowledgeItem

class WokSpider(scrapy.Spider):
    name = "wok"
    allowed_domains = ["webofknowledge.com"]
    start_urls = (
        'http://www.webofknowledge.com/',
    )

    sid = 'U2ms4jJ5ZQ51CJZrItz'
    query_id = 1
    num_docs = 10

    def start_requests(self):
        '''
        username = 'your@email.com'
        password = 'pass****'

        url1 = "http://wos.fecyt.es/"
        resp = requests.get(url1)

        url2 = resp.url

        import urlparse

        parsed = urlparse.urlparse(url2)
        print urlparse.parse_qs(parsed.query)['SAMLRequest']


        params = {'adAS_mode':'authn', 'adAS_username': username, 'adAS_password':password}
        resp2 = requests.post(url2,data=params)
        '''
        
        docs = range(1,self.num_docs)
        for doc in docs:
            url = 'http://apps.webofknowledge.com/full_record.do?product=UA&search_mode=AdvancedSearch&SID={0}&qid={1}&doc={2}'
            callback = self.parse

            yield scrapy.Request(url.format(self.sid,self.query_id,doc), callback=callback)

    def parse(self, response):
        
        item = WebofknowledgeItem()
        tit_value = response.xpath('//div[@class="title"]/value/text()').extract()
        tit_item = response.xpath('//div[@class="title"]/item/text()').extract()

        if (len(tit_value) > 0):
            item['titulo'] = tit_value[0]
        elif (len(tit_item) > 0):
            item['titulo'] = tit_item[0]
        else:
            item['titulo'] = "Sin título"

        item['url'] = response.url
        item['citas'] = response.xpath('//span[@class="TCcountFR"]/text()').extract()[0]
        # item['issn'] = response.xpath('//*[contains(text(),"ISSN:")]/../text()').extract()

        issn_value = response.xpath('//*[text()="ISSN:"]/../value/text()').extract()
        if  (len(issn_value)>0):
            item['issn'] = response.xpath('//*[text()="ISSN:"]/../value/text()').extract()
        else:
            item['issn'] = response.xpath('//*[text()="ISSN:"]/../text()').extract()[1]
        

        yield item

