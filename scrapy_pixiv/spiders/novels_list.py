import json
import logging

import scrapy


class NovelsListSpider(scrapy.Spider):
    name = "novels-list"
    allowed_domains = ["pixiv.net"]

    lastIds = [
        # 2e8 + 3e7,
        23171313,
    ]
    
    def make_request(self, lastId):
        self.log(f'lastId: {lastId}', logging.INFO)
        yield scrapy.Request(
                url=f"https://www.pixiv.net/ajax/novel/new?lastId={lastId}&limit=20&r18=false&lang=en&version=de0cfe5bb0022b2e28b14b73cc3097f56382a23b",
                cookies={'PHPSESSID': '110304626_AowvulN2SRW3fYPsxQuKRFuvP4I62k8C'}
            )

    def start_requests(self):
        for lastId in self.lastIds:
            yield from self.make_request(lastId)

    def parse(self, response: scrapy.http.response.Response):
        data = json.loads(response.body)
        if data['error']:
            raise Exception(data['message'])
        
        for item in data['body']['novels']:
            yield item

        lastId = data['body']['lastId']
        yield from self.make_request(lastId)

        

