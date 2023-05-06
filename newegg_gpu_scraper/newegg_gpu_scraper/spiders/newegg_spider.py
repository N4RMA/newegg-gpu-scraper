import scrapy


class NeweggSpiderSpider(scrapy.Spider):
    name = "newegg_spider"
    allowed_domains = ["newegg.ca"]
    start_urls = ["https://www.newegg.ca/GPUs-Video-Graphics-Cards/SubCategory/ID-48"]

    def parse(self, response):
        products = response.xpath("//div[contains(@class, 'item-cell')]")

        for product in products:
            name = product.xpath(".//a[contains(@class, 'item-title')]/text()").get()
            price_whole_part = product.xpath(".//li[contains(@class, 'price-current')]/strong/text()").get()
            price_fraction_part = product.xpath(".//li[contains(@class, 'price-current')]/sup/text()").get()
            price = f'{price_whole_part}{price_fraction_part}'
            url = product.xpath(".//a[contains(@class, 'item-title')]/@href").get()

            # Yield the extracted data as a dictionary
            yield {
                'name': name,
                'price': price,
                'url': url,
            }

        # Locate and follow the next page link, if available
        next_page_url = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
