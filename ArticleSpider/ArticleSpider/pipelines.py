# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for pk,value in results:
                image_file_path = value["path"]
            item['front_image_path'] = image_file_path
        return item


# 自定义json文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

# 使用scrapy自带的ＪsonItemExporter
class JsonExporterPipeline(object):
    #调用scrapｙ提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexporter.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

import pymysql
pymysql.install_as_MySQLdb()


def MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('192.168.10.219','root','huang921118','article_spider',charset='utf8',user_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = """
        insert into jobbole_article(title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["url"],item["create_date"],item["fav_nums"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicoe = True,
        )

        dbpool = adbapi.ConnectionPool("pymsql",**dbparms)

        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrorback(self.handle_error,item,spider)

    def handle_error(self,failture,item,spider):
        print(failture)

    def do_insert(self,cursor,item):
        insert_sql = """
        insert into jobbole_article(title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s)
        """
        cursor.execute(insert_sql,(item["title"],item["url"],item["create_date"],item["fav_nums"]))
