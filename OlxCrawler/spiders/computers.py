# -*- coding: utf-8 -*-
import scrapy


class ComputersSpider(scrapy.Spider):
    name = 'computers'
    allowed_domains = ['olx.com.br']
    start_urls = ['https://olx.com.br/computadores-e-acessorios']

    def parse(self, response):
        pcs = response.xpath('//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]')
        for i in pcs:
            links = i.xpath('./a/@href').extract_first()
            yield scrapy.Request(url = links, callback = self.cb)
        prox = response.xpath('//li[contains(@class, "item next")//a[@rel = "next"]/@href]').extract_first()
        if prox:
            self.log(f'Próxima Página: {prox}')
            yield scrapy.Request(url = prox, callback = self.parse)
    def cb(self, response):
        titulo = response.xpath('//*[@id="root"]/div[4]/div/div[1]/div[2]/div[1]/div[6]/h1/text()').extract_first()
        custo = response.xpath('//*[@id="root"]/div[4]/div/div[1]/div[2]/div[2]/div[7]/div/div[1]/div[2]/h2/text()').extract_first()
        yield {'titulo': titulo, 'custo': custo}
