from scrapy.spider import BaseSpider

class WikiSpider(BaseSpider):
  name = "wiki"
  allowed_domains = ["en.wikipedia.org"]
  start_urls = [
    "http://en.wikipedia.org"
  ]

  def parse(self, response):
    filename = response.url.split("/")[-2]
    open(filename, 'wb').write(response.body)
