import json
import logging

import scrapy


class NovelsDetailSpider(scrapy.Spider):
    name = "novels-detail"
    allowed_domains = ["pixiv.net"]
    
    def make_request(self, novelId):
        yield scrapy.Request(
                url=f"https://www.pixiv.net/ajax/novel/{novelId}",
                # cookies={'PHPSESSID': '110304626_AowvulN2SRW3fYPsxQuKRFuvP4I62k8C'}
            )

    def start_requests(self):
        start_id = 23137858

        for lastId in range(start_id - 60 * 60 * 10, start_id):
            yield from self.make_request(lastId)

    def parse(self, response: scrapy.http.response.Response):
        data = json.loads(response.body)
        if data['error']:
            raise Exception(data['message'])
        
        item = data['body']
        self.log(f'scraped Item(id={item["id"]}, title={item["title"]})', logging.INFO)
        item['coll'] = 'pixiv-novel-detail'
        yield item