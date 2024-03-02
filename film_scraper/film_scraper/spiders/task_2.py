import scrapy
from urllib.parse import urljoin
from scrapy.http import TextResponse


class Ex2Spider(scrapy.Spider):
    name = "hockey_spider"
    allowed_domains = ['scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/forms/']

    async def parse(self, response, **kwargs):
        if not isinstance(response, TextResponse):
            response = TextResponse(url=response.url, body=response.body, encoding='utf-8')
        yield scrapy.FormRequest.from_response(
            response,
            formdata={"q": "New York"},
            callback=self.responsed
        )

    async def responsed(self, response):
        for pages_link in response.xpath(
                '//section/div/div[5]/div[1]/ul/li/a[not(@aria-label="Next")]/@href').extract():
            yield scrapy.Request(urljoin(response.url, pages_link), callback=self.parse_page)

    async def parse_page(self, response):
        table_rows = response.xpath('//table/tr')
        headers = [value.strip() for value in table_rows[0].xpath('./th//text()').extract()]
        for row in table_rows[1:]:
            data = [value.strip() for value in row.xpath('./td//text()').extract()]
            yield dict(zip(headers, data))
