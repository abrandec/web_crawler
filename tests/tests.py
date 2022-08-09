""" Web Crawler Unit Tests """
import os
import logging
import pytest
from web_crawler.module import web_crawler

@pytest.fixture
def setup():
    pass

def test_download_simple():
    """ Test retrieving links """
    timeout = 5
    no_go_domains = ['facebook.com', 'youtube.com']
    max_depth = 1
    save_dest = './tests/test_downloads'
    crawler = web_crawler(timeout, no_go_domains, max_depth, save_dest, False)
    saved_urls = []
    saved_dests = []

    saved_urls, saved_dests = crawler.crawl(["http://www.twitter.com"])
    print(saved_dests)
    for dest in saved_dests:
        assert os.path.exists(dest) == True
    print("✅ All files saved - PASS")

def test_links():
    pass