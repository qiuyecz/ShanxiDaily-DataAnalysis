import scrapy

from ICourse.items import IcourseItem

class IcourseSpider(scrapy.Spider):
    name = "icourse"
    allowed_domains = ["news.sxrb.com"]
    start_urls = ["http://news.sxrb.com/GB/314060/index10.html"]

    def parse(self, response):
        node_list = response.xpath("//div[@class='mod_bd clearfix on']/ul/li")
        for node in node_list:
            # 创建item字段对象，用来存储信息
            item = IcourseItem()
            # .extract() 将xpath对象转换围殴Unicode字符串
            name = node.xpath("./div[@class='tail']/span/a/text()").extract()
            title = node.xpath("./h3/a/text()").extract()
            info = node.xpath("./p/text()").extract()
            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]
            # 返回提取到的每一个item数据 给管道文件处理，同时还会回来继续执行后面的代码
            yield item
