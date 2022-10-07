import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()


class DisplaySpider(scrapy.Spider):
    name = 'xxrsm'
    start_urls = ['https://xxrsm.com']
    titleArr = ['色域容积', '常规亮度', '响应速度', '均匀度', '对比度', 'HDR峰值亮度']
    productList = []

    def parse(self, response):
        div_list = response.css('div.item.tab_item.formTabCntId')
        for index, selector in enumerate(div_list):
            title = self.titleArr[index]
            items = selector.css('#routeView > tbody > tr')
            tempList = []
            for i, item in enumerate(items):
                score = 1000 - i
                name = item.css('td:nth-child(2)').css('li::text').get()
                foundTemp = False
                for temp in tempList:
                    if temp['name'] == name:
                        foundTemp = True
                if not foundTemp:
                    found = False
                    for product in self.productList:
                        if product['name'] == name:
                            product['score'] += score
                            found = True
                    if not found:
                        self.productList.append(Product(name=name, score=score))
                    tempList.append(Product(name=name, score=score))
        yield {'list': sorted(self.productList, key=lambda x: -x['score'])}
