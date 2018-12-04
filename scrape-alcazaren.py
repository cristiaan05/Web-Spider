#!/usr/bin/python
# coding=utf-8

import scrapy, logging
from scrapy.http import FormRequest
from scrapy.contrib.spiders import CrawlSpider, Rule

class KSpider(scrapy.Spider):
    name = 'alcazaren-spider'
    start_urls = ['https://alcazaren.com.gt/catalogo-alcazaren/']

    def parse(self, response):
        return [FormRequest(url="https://alcazaren.com.gt/catalogo-alcazaren/", cookies={'edad_valida':'true'}, callback=self.parse_categories)]

    def parse_categories(self, response):
        for category in response.css('.product-category1 a'):
            link = category.css('::attr("href")').extract()[0]
            cat_name = category.css('h3::text').extract()[0]
            print(link, cat_name)
            yield scrapy.Request(link, self.parse_subcategories, meta={'category':cat_name})

    def parse_subcategories(self, response):
        for category in response.css('.product-category a'):
            link = category.css('::attr("href")').extract()[0]
            cat_name = category.css('h3::text').extract()[0]
            print(link, cat_name, "\n\n\n\n\n\n-------------------------------------------\n\n\n\n\n\n\n\n")
            yield scrapy.Request(link, self.parse_products, meta={'category':cat_name})

    def parse_products(self, response):
        for page in response.css('.pagination li a::attr("href")').extract():
            yield scrapy.Request(page, self.parse_products, meta={'category':response.meta['category']})
        for product in response.css('.product-item'):
            link = product.css('a::attr("href")').extract()[0]
            yield scrapy.Request(link, self.parse_product, meta={'category':cat_name})
                

    def parse_product(self, response):
        name = product.css('div.divider-sm > h3 > a > p::text').extract()
        name = ",".join(name)
        sku = product.css('div.product_meta >span.sku_wrapper span::text').extract()
        sku= ",".join(sku)
        img= product.css('div.product-single-image a::attr("href")').extract()
        desc= product.css('div.product-description > p::text').extract()
        desc= ",".join(desc)
        cat= product.css('div.product_meta > span.posted_in > a::atrr("href")').extract()
        cat= ",".join(cat)
        tags= product.css('div.product_meta > span.tagged_as > a::atrr("href"').extract()
        tags= ",".join(tags)
        stock= product.css('span.stock_class ::text').extract()
        stock = False
        if stock_string == 'Disponible en Stock':
            stock = True

        yield {
            'name': name,
            'sku': sku,
            'img': img,
            'desc': desc,
            'cat': cat,
            'tags': tags,
            'stock': stock
        }

        
