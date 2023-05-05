import scrapy


class NeweggSpiderSpider(scrapy.Spider):
    name = "newegg_spider"
    allowed_domains = ["newegg.ca"]
    start_urls = ["http://newegg.ca/"]

    def parse(self, response):
        pass
