import pprint
import unittest
import app.news.feeds as feeds
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

class TestFeeds(unittest.TestCase):

    def test_autoblog_feed(self):
        feed = feeds.autoblog_feed()
        # pp.pprint(feed)
        # soup = BeautifulSoup(feed[0]['summary'], 'html.parser')
        # print soup.text


    def test_autoblog_make_feed(self):
        feed = feeds.autoblog_make_feed('Honda')
        pp.pprint(feed)

    def test_motortrend_feed(self):
        feed = feeds.motortrend_feed()
        pp.pprint(feed)

    def test_motortrend_make_feed(self):
        pass