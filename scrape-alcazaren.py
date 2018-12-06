#!/usr/bin/python
# coding=utf-8
# encoding=utf8

import scrapy, logging
from scrapy.http import FormRequest
from scrapy.contrib.spiders import CrawlSpider, Rule

class KSpider(scrapy.Spider):
    name = 'alcazaren-spider'
    start_urls = ['https://alcazaren.com.gt/catalogo-alcazaren/']
    handle_httpstatus_list = [400, 302]
    def parse(self, response):
        #formdata = {'log': 'chtello05@gmail.com','pwd': 'Kemik2018' }
        return [FormRequest(url="https://alcazaren.com.gt/catalogo-alcazaren", cookies={'edad_valida':'true'},callback=self.parse_categories)]
        #return [FormRequest(url="https://alcazaren.com.gt/catalogo-alcazaren", cookies={'edad_valida':'true'},clickdata={'name':'user-submit'},callback=self.parse_categories)]

    def parse_categories(self, response):
        for category in response.css('.menu-categorias-container ul li'):
            link = category.css('a::attr("href")').extract()[0]
            cat_name = category.css('a::text').extract()[0]
            yield scrapy.Request(link,callback=self.parse_products)
            print('Login',link)

    def parse_products(self, response):
        for page in response.css('.pagination a::attr("href")').extract():
            yield scrapy.Request(page, self.parse_products)
        for product in response.css('.product-item div h3 a'):
            link = product.css('::attr("href")').extract()[0]
            prod_name = product.css('p.prin::text').extract()[0]
            yield scrapy.Request(link,callback=self.parse_description, meta={'category':prod_name})         
    
    def parse_description(self, response):
            prod_desc = ' '.join(response.css('div.product-description > div > p::text').extract())
            name = ' '.join(response.css('div.product-title > p.prin::text').extract())
            sec = ' '.join(response.css('div.product-title > p.sec::text').extract())
            terc = ' '.join(response.css('div.product-title > p.terc::text').extract())
            sku = ' '.join(response.css('div.product_meta > span.sku_wrapper > span::text').extract())
            category = ' '.join(response.css('div.product_meta > span.posted_in > a::text').extract())
            tags = '  '.join(response.css('div.product_meta > span.tagged_as > a::text').extract())
            img = '  '.join(response.css('div.product-single-image img::attr("src")').extract())
            price = ' '.join(response.css('div.summary entry-summary >span.price nottached >span::text').extract())
            #img = ' '.join(response.css('a.product-mask > div.product-thumb > img.attachment-shop_catalog size-shop_catalog wp-post-image animated fadeIn'))
            for  item in prod_desc:
                item = item.encode('utf-8')     
            yield{
                'categorias': prod_desc.replace('\n',''),
                'name': name.replace('\n', ''),
                'sec': sec.replace('\n',''),
                'terc': terc.replace('\n', ''),
                'sku': sku.replace('\n', ''),
                'category': category.replace('\n', ''),
                'tags': tags.replace('\n', ''),
                'img': img.replace('\n', ''),
                'price': price.replace('\n', ''),                     
            }
            #if stock_string == 'Disponible en Stock':
            #stock = True

        
