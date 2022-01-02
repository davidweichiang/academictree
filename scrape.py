import scrapy, scrapy.crawler
import re, collections

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = collections.defaultdict(dict)

class TreeSpider(scrapy.Spider):
    name = "tree"
    def __init__(self, start_id, graph, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_id = start_id
        self.graph = graph

    def start_requests(self):
        ids = [self.start_id]
        for i in ids:
            url = f'https://academictree.org/neurotree/peopleinfo.php?pid={i}'
            yield scrapy.Request(url=url, callback=self.parse, meta={'id':i})

    def parse(self, response):
        self_id = response.meta['id']
        for h in response.xpath('//h1/text()'):
            name = h.extract().strip()
        self.graph.nodes[self_id] = {
            'name': name,
            'url': response.url,
        }
        for div in response.xpath('//div[h4/text()="Parents"]'):
            for a in div.xpath('.//a'):
                url = a.attrib['href']
                if m := re.search(r'peopleinfo\.php\?pid=(\d+)$', url):
                    parent_id = m.group(1)
                    self.graph.edges[parent_id][self_id] = {}
                    yield scrapy.Request(url=response.urljoin(url), callback=self.parse, meta={'id': self_id})

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('start_id', help='Numeric ID of person whose ancestry to crawl')
    ap.add_argument('output', help='File to write DOT file to')
    args = ap.parse_args()
    
    g = Graph()
    c = scrapy.crawler.CrawlerProcess()
    c.crawl(TreeSpider, args.start_id, g)
    c.start()

    with open(args.output, 'w') as outfile:
        print('digraph {', file=outfile)
        print('  node [shape=box]', file=outfile)
        for i, info in g.nodes.items():
            name = info['name']
            url = info['url']
            print(f'  {i} [label="{name}",URL="{url}"]', file=outfile)
        for u in g.edges:
            for v in g.edges[u]:
                print(f'  {u} -> {v}', file=outfile)
        print('}', file=outfile)
    
    
