# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider


# class DdSpider(scrapy.Spider):
class DdSpider(RedisSpider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = "dd:request"

    def parse(self, response):
        div_lsit = response.xpath("//div[@class='con flq_body']/div")[1:-1]

        for div in div_lsit:
            item = {}
            item["o_title"] = div.xpath(".//dl[contains(@class, 'primary_dl')]/dt//text()").extract_first()
            dl_list = div.xpath(".//dl[@class='inner_dl']")
            for dl in dl_list:
                item["t_title"] = dl.xpath("./dt//text()").extract()
                dd_lsit = dl.xpath("./dd/a")
                for dd in dd_lsit:
                    item["s_title"] = dd.xpath("./text()").extract_first()
                    item["s_href"] = dd.xpath("./@href").extract_first()
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_list(self, response):
        item = response.meta["item"]
        div_list_l = response.xpath("//div[@id='search_nature_rg']/ul/li")
        for div_l in div_list_l:
            item["f_title"] = div_l.xpath("./a/@title").extract_first()
            item["img"] = div_l.xpath("./a/img/@src").extract_first()
            item["f_href"] = div_l.xpath("./a/@href").extract_first()
            item["author"] = div_l.xpath("./p[5]/span[1]//text()").extract()
            item["date"] = div_l.xpath("./p[5]/span[2]/text()").extract_first()
            item["local"] = div_l.xpath("./p[5]/span[3]//text()").extract()
            item["require"] = div_l.xpath("./p[4]/a/text()").extract_first()
            item["price"] = div_l.xpath(".//p/span[@class='search_now_price']/text()").extract_first()
            item["merchant"] = div_l.xpath("./div[1]/span/span/text()").extract_first()
            item["merchant"] = "当当自营" if item["merchant"] is None else item["merchant"]
            print(item)
            yield item

        next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_url is not None:
            yield response.follow(
                next_url,
                callback=self.parse_list,
                meta={"item": item}
            )
    # def parse(self, response):
    #     #获取大分类分组
    #     div_list = response.xpath("//div[@class='con flq_body']/div")[1:-1]
    #     for div in div_list:
    #         item = {}
    #         #大分类的名字
    #         item["b_cate"] = div.xpath(".//dl[contains(@class,'primary_dl')]/dt//text()").extract()
    #         #获取中间分类的分组
    #         dl_list = div.xpath(".//dl[@class='inner_dl']")
    #         for dl in dl_list:
    #             #中间分类的名字
    #             item["m_cate"] = dl.xpath("./dt//text()").extract()
    #             #获取小分类的分组
    #             a_list = dl.xpath("./dd/a")
    #             for a in a_list:
    #                 #小分类的名字
    #                 item["s_cate"] = a.xpath("./text()").extract_first()
    #                 item["s_href"] = a.xpath("./@href").extract_first()
    #                 #发送小分类URL地址的请求，达到列表页
    #                 yield scrapy.Request(
    #                     item["s_href"],
    #                     callback=self.parse_book_list,
    #                     meta = {"item":deepcopy(item)}
    #                 )
    #
    # def parse_book_list(self,response): #提取列表页的数据
    #     item = response.meta["item"]
    #     #获取列表页图书的分组
    #     li_list = response.xpath("//ul[@class='bigimg']/li")
    #     for li in li_list:
    #         item["book_name"] = li.xpath("./a/@title").extract_first()
    #         item["book_href"] = li.xpath("./a/@href").extract_first()
    #         item["book_author"] = li.xpath(".//p[@class='search_book_author']/span[1]/a/text()").extract()
    #         item["book_press"] = li.xpath(".//p[@class='search_book_author']/span[3]/a/text()").extract_first()
    #         item["book_desc"] = li.xpath(".//p[@class='detail']/text()").extract_first()
    #         item["book_price"] = li.xpath(".//span[@class='search_now_price']/text()").extract_first()
    #         item["book_store_name"] = li.xpath(".//p[@class='search_shangjia']/a/text()").extract_first()
    #         item["book_store_name"] = "当当自营" if item["book_store_name"] is None else item["book_store_name"]
    #         yield item
    #
    #     #实现列表页翻页
    #     next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
    #     if next_url is not None:
    #         #构造翻页请求
    #         yield response.follow(
    #             next_url,
    #             callback = self.parse_book_list,
    #             meta = {"item":item}
    #         )