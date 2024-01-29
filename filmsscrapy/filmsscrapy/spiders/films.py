import scrapy
from filmsscrapy.items import FilmsscrapyItem
import time


def get_table(table):
    span = table.css('span')
    a_tags = span.css('a')
    if a_tags:
        text_list = a_tags.css('::text').getall()
        all_text = ', '.join(set(text_list))
    else:
        all_text = span.css('::text').get()
    return all_text


class FilmsSpider(scrapy.Spider):
    name = "films"
    

    def start_requests(self):
        URL = "https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"
        yield scrapy.Request(url=URL, callback=self.parse_page)

    #parse each page
    def parse_page(self, response):

        for selector in response.css('div#mw-pages li'):
            selector.css('::text').get()
            film_url = "https://ru.wikipedia.org/" + selector.css('a::attr(href)').get()
            yield response.follow(film_url, callback=self.parse_film)

        next_page = response.xpath('//a[text()="Следующая страница"]/@href').get()

        if next_page:
            next_url = "https://ru.wikipedia.org/" + next_page
            yield response.follow(next_url, callback=self.parse_page)

    #parse parametrs for each film
    def parse_film(self, response):

        item = FilmsscrapyItem()
        item['title'] = response.css('th::text').get()
        item['genre'] = get_table(response.css('tr:contains("Жанры"), tr:contains("Жанр")'))
        item['director'] = get_table(response.css('tr:contains("Режиссёры"), tr:contains("Режиссёр")'))
        item['country'] = get_table(response.css('tr:contains("Страна"), tr:contains("Страны")'))
        item['year'] = get_table(response.css('tr:contains("Год")'))
        item['rating'] = None

        raiting_link = response.css('tr:contains("IMDb") span a::attr(href)').get()
        time.sleep(1.5)
        if raiting_link:
            yield scrapy.Request(raiting_link, callback=self.parse_rating, meta={'item': item})
        else:
            yield item

    #parse rating from IMDb
    def parse_rating(self, response):
        item = response.meta['item']
        item['rating'] = response.css('div.sc-acdbf0f3-0 span.sc-bde20123-1::text').get()

        yield item

