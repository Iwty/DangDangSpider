# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DangdPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "dd":
            item["o_title"] = "".join([i.strip() for i in item["o_title"]])
            item["t_title"] = "".join([i.strip() for i in item["t_title"]])
            print(item)
        return item
