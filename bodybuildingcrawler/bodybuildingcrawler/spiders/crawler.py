import scrapy
import requests
from bs4 import BeautifulSoup
from bodybuildingcrawler.items import BodybuildingcrawlerItem

#from fitness.items import FitnessItem

class BBArticleCrawler(scrapy.Spider):
    #new_path = '/users/TimLin/fitness/fitness/test.txt'
    #os.remove(new_path) if os.path.exists(new_path) else None
    name = 'BBCrawler'
    start_urls=['http://www.exrx.net/Lists/Directory.html']

    def parse(self,  response):
        domain = "https://search.bodybuilding.com/slp/full?query="
        searchterm = 'glutes'
        page = 1
        while True:
            url = domain + searchterm + '&context=articles&page=' + str(page) + '&size=100'
            print(url, "\n\n")
            req = requests.get(url)
            res = BeautifulSoup(req.text,'lxml')
            if len(res.select('.bb-article-listing__header')) == 0:
                break
            else:
                yield  scrapy.Request(url, self.parse_detail)
                page = page + 1

    def parse_detail(self, response):
        res = BeautifulSoup(response.body, 'lxml')
        #if len(res.select('.bb-article-listing__header')) == 0:
        for items in res.select('.bb-article-listing__header'):
            yield  scrapy.Request(items['href'], self.parse_detail_l2)

    def parse_detail_l2(self, response):
        res = BeautifulSoup(response.body, 'lxml')
        bbitem = BodybuildingcrawlerItem()
        bbitem['classification'] = 'Glutes'
        bbitem['title'] = res.select('.main-header')[0].text #title
        article = ""
        for items in res.select('p'):
            article += items.text.replace('\n','').replace('\r','').replace('   ','') #article content
        bbitem['content'] = article #title
        return bbitem
