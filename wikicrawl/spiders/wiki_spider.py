from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy.exceptions import CloseSpider

from wikicrawl.items import WikicrawlItem

class WikiSpider(CrawlSpider):
  name = "wiki"
  allowed_domains = ["en.wikipedia.org"]
  start_urls = [ ]

  article_rule = SgmlLinkExtractor(allow=('/wiki/[A-Za-z_()]+$', ))
  default_rule = SgmlLinkExtractor(allow=('/.*', ))

  rules = (
    Rule(WikiSpider.article_rule, callback='parse_article'),
    Rule(WikiSpider.default_rule, follow=False),
  )

  def __init__(self, *args, **kwargs):
    super(WikiSpider, self).__init__(*args, **kwargs)

    self.start_url = 'http://en.wikipedia.org/wiki/%s' % kwargs.get("start")
    self.goal_url = 'http://en.wikipedia.org/wiki/%s' % kwargs.get("goal")

    if not cmd_start: raise ValueError("Must provide a start url!")
    self.start_urls = [self.start_url]

    self.items = {}
    self.parents = {}
    self.root = WikicrawlItem(link=self.start_url, min_depth=0)
    self.item_map[self.start_url] = self.root

  def fetch_item(self, url):
    return self.items.setdefault(url,
      WikicrawlItem(link=self.start_url, min_depth=9999))

  def parse_article(self, response):
    item = self.fetch_item(response.url)
    hxs = HtmlXPathSelector(response)

    if response.url in self.parents:
      parents = self.parents[response.url]
      for parent in parents:
        item['min_depth'] = min(item['min_depth'], parent['min_depth'] + 1)
    else:
      item['min_depth'] = 0

    raise CloseSpider("Debug.")
