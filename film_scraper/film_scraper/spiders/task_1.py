import scrapy
import json

class FilmSpider(scrapy.Spider):
    name = 'film_spider'
    allowed_domains = ['scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/ajax-javascript/']

    async def parse(self, response, **kwargs):
        years = response.xpath('//section/div/div[4]/div/a/text()').extract()
        for year in years:
            yield scrapy.Request(
                f'https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={year}',
                cb_kwargs={'year': year},
                callback=self.parse_films
            )

    async def parse_films(self, response, **kwargs):
        item = {
            'year': kwargs['year'],
            'films': response.json(),
        }
        yield item
