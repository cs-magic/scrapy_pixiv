import json

import scrapy


class NovelsSpider(scrapy.Spider):
    name = "novels"
    allowed_domains = ["pixiv.net"]

    lastIds = [
        # 2e8 + 3e7,
        # 23171313,
        23170312,
    ]
    start_urls = [
        f"https://www.pixiv.net/ajax/novel/new?lastId={lastId}&limit=20&r18=false&lang=en&version=de0cfe5bb0022b2e28b14b73cc3097f56382a23b"
        for lastId in lastIds
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                cookies={'PHPSESSID': '110304626_AowvulN2SRW3fYPsxQuKRFuvP4I62k8C'}
            )

    def parse(self, response: scrapy.http.response.Response):
        data = json.loads(response.body)
        if data['error']:
            raise Exception(data['message'])
        
        for item in data['body']['novels']:
            yield item
