#!/usr/bin/python
# coding=utf-8
# encoding=utf8

import scrapy, logging
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule



class KSpider(scrapy.Spider):
    name = 'alcazaren-spider'
    start_urls = ['https://alcazaren.com.gt/catalogo-alcazaren']
    handle_httpstatus_list = [400, 302]
    def parse(self, response):
        return [FormRequest(url="https://alcazaren.com.gt/wp-login.php", cookies={'edad_valida':'true'}, callback=self.parse_login)]

    def parse_login(self, response):
        print('Si entrto')
        #key= response.css('input[name="security"]::attr(value)').extract_first()
        return [FormRequest(url='https://alcazaren.com.gt/wp-login.php', 
        formdata={'log': 'chtello05@gmail.com', 'pwd': 'Kemik2018','testcookies':'1'},
        method='POST', 
        callback=self.parse_afterlogin)] 

    def parse_afterlogin(self, response):
        print('HOlaaaa')
        yield scrapy.Request('https://alcazaren.com.gt/catalogo-alcazaren',callback=self.parse_categories)

    def parse_categories (self, response):
        print('entre al catalogo')
        for category in response.css('.menu-categorias-container ul li'):
            link = category.css('a::attr("href")').extract()[0]
            cat_name = category.css('a::text').extract()[0]
            yield scrapy.Request(link,callback=self.parse_products)

    def parse_products(self, response):
        for page in response.css('.pagination a::attr("href")').extract():
            yield scrapy.Request(page, self.parse_products)
        for product in response.css('.product-item div h3 a'):
            link = product.css('::attr("href")').extract()[0]
            prod_name = product.css('p.prin::text').extract()[0]
            yield scrapy.Request(link,callback=self.parse_description, meta={'category':prod_name})         
    
    def parse_description(self, response):
            prod_desc = ''.join(response.css('div.product-description > div > p::text').extract())
            name = ''.join(response.css('div.product-title > p.prin::text').extract())
            sec = ''.join(response.css('div.product-title > p.sec::text').extract())
            terc = ''.join(response.css('div.product-title > p.terc::text').extract())
            sku = ' '.join(response.css('div.product_meta > span.sku_wrapper > span::text').extract())
            category = ' '.join(response.css('div.product_meta > span.posted_in > a::text').extract())
            tags = ' '.join(response.css('div.product_meta > span.tagged_as > a::text').extract())
            img = '  '.join(response.css('div.product-single-image img::attr("src")').extract())
            price = ' '.join(response.css('span > span::text').extract()[1])
            stock= ' '.join(response.css('span.stock_class2::text').extract())
            for  item in prod_desc:
                item = item.encode('utf-8')        
            yield{
                'categorias': prod_desc.replace('\n', ''),
                'name': name.replace('\n', ''),
                'sec': sec.replace('\n', ''),
                'terc': terc.replace('\n', ''),
                'sku': sku.replace('\n', ''),
                'category': category.replace('\n', ''),
                'tags': tags.replace('\n', ''),
                'img': img.replace('\n', ''),
                'price': price.replace('\n', ''),                     
                'stock': stock.replace('\n', ''),                          
            }
