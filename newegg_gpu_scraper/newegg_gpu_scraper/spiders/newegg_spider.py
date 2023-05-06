import scrapy


class NeweggSpiderSpider(scrapy.Spider):
    name = "newegg_spider"
    allowed_domains = ["newegg.ca"]
    start_urls = ["https://www.newegg.ca/GPUs-Video-Graphics-Cards/SubCategory/ID-48/Page-1"]

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

        # Extract the current page number and increment it to get the next page number
        current_page_number = int(response.url.split('Page-')[-1])
        next_page_number = current_page_number + 1

        # Generate the next page URL by replacing the page number in the current URL
        next_page_url = response.url.replace(f'Page-{current_page_number}', f'Page-{next_page_number}')

        # Follow the next page link
        yield scrapy.Request(url=next_page_url, callback=self.parse)
