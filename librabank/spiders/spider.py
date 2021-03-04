import scrapy

from scrapy.loader import ItemLoader
from ..items import LibrabankItem
from itemloaders.processors import TakeFirst


class LibrabankSpider(scrapy.Spider):
	name = 'librabank'
	start_urls = ['https://www.librabank.ro/Stiri/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="leftColumn"]/h3/text()').get()
		description = response.xpath('//div[@class="leftColumn"]/table//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@align="right"]/span[@style]/text()').get()

		item = ItemLoader(item=LibrabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
