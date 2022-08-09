""" Web Crawler Examples """
from web_crawler.module import web_crawler

def example_crawler():
    """ Web Crawler Example """
    timeout = 5
    no_go_domains = ['http://facebook.com', 'http://youtube.com']
    max_depth = 1
    save_dest = './example/example_downloads'
    crawler = web_crawler(timeout, no_go_domains, max_depth, save_dest, True)
    crawler.crawl(["http://www.twitter.com", 'http://facebook.com', 'http://youtube.com'])

if __name__ == '__main__':
    example_crawler()
