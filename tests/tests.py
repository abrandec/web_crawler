""" Web Crawler Unit Tests """
import os
import pytest
from web_crawler.module import web_crawler

# pylint: disable=unnecessary-pass

@pytest.fixture
def setup():
    """ Setup dummy data """
    pass

def test_download_simple():
    """ Test retrieving links """
    timeout = 5
    no_go_domains = ['facebook.com', 'youtube.com']
    max_depth = 1
    save_dest = './tests/test_downloads'
    crawler = web_crawler(timeout, no_go_domains, max_depth, save_dest, False)
    saved_dests = []
    _, saved_dests = crawler.crawl(["http://www.twitter.com"])
    for dest in saved_dests:
        assert os.path.exists(dest) is True
    print("✅ All files saved - PASS")
    