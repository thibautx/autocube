import pprint
import unittest

pp = pprint.PrettyPrinter(indent=4)

class TestFeeds(unittest.TestCase):

    def test_autoblog_feed(self):
        feed = sadf.autoblog_feed()
        # pp.pprint(feed)
        # soup = BeautifulSoup(feed[0]['summary'], 'html.parser')
        # print soup.text


    def test_autoblog_make_feed(self):
        feed = sadf.autoblog_make_feed('Honda')
        pp.pprint(feed)

    def test_motortrend_feed(self):
        feed = sadf.motortrend_feed()
        pp.pprint(feed)

    def test_motortrend_make_feed(self):
        pass

# import pprint
#
# import feedparser as fp
# from bs4 import BeautifulSoup
#
# # from app.news.sadf.autoblog import format_entry
# # from app.news.sadf.autoweek import format_autoweek_entry
#
# pp = pprint.PrettyPrinter(indent=2)
#
# def parse_feed(url, source, make_feed=False):
#     entries = fp.parse(url)['entries']
#     # f_format = formatters[blog]
#     return [format_entry(entry, source) for entry in entries]
#     # return [f_format(entry, make_feed=make_feed) for entry in entries]
#
#
# # def format_entry(entry, source):
# #     soup = BeautifulSoup(entry['summary'], 'html.parser')
# #     try:
# #         image = soup.find('img').attrs['src']
# #     except:
# #         image = None
# #
# #     summary = BeautifulSoup(entry['summary'], 'html.parser').text
# #
# #     formatted = {
# #         'source': source,
# #         'title': entry['title'],
# #         'author': entry['author'],
# #         'link': entry['link'],
# #         'date': entry['published'],
# #         'summary': summary,
# #         'image': image if image is not None else 'http://placehold.it/1000x1000.jpg',
# #     }
# #     return formatted
#
#
# # MOTORTREND
# def motortrend_feed(make=None):
#     # url = 'http://www.motortrend.com/widgetrss/motortrend-stories.xml'
#     url = 'http://www.motortrend.com/feed/'
#     return parse_feed(url, source='motortrend')
#
#
# def motortrend_make_feed(make):
#     pass
#
#
# def format_motortrend_entry(entry, make_feed=False):
#     soup = BeautifulSoup(entry['summary'], 'html.parser')
#     try:
#         image = soup.find('img').attrs['src']
#     except:
#         image = None
#
#     summary = BeautifulSoup(entry['summary'], 'html.parser').text
#
#     formatted = {
#         'title': entry['title'],
#         'author': entry['author'],
#         'link': entry['link'],
#         'date': entry['published'],
#         'summary': summary,
#         'image': image,
#     }
#
#     return formatted
#
#
# # CAR AND DRIVER (doesn't work?? no rss feed)
# def caranddriver_feed(make=None):
#     url = 'http://feeds.feedburner.com/caranddriver/blog.xml'
#     return parse_feed(url, 'caranddriver')
#
#
# def format_caranddriver_entry(entry):
#     soup = BeautifulSoup(entry['summary'], 'html.parser')
#     try:
#         image = soup.find('img').attrs['src']
#     except:
#         image = None
#
#     summary = BeautifulSoup(entry['summary'], 'html.parser').text
#     print summary
#
#     formatted = {
#         'title': entry['title'],
#         'author': entry['author'],
#         'link': entry['link'],
#         'date': entry['published'],
#         'summary': summary,
#         'image': image,
#     }
#
#     return formatted
#
#
# # TOPGEAR (doesn't work?? no rss feed)
# def topgear_feed():
#     pass
#
#
# def thecarconnection_feed():
#     url = 'http://feeds.highgearmedia.com/?sites=TheCarConnection&type=all'
#     return parse_feed(url)
#
#
# def automobilemag_feed():
#     url = 'http://www.automobilemag.com/news/feed/'
#     return parse_feed(url)
#
#
# # formatters = {
# #     'autoblog': format_autoblog_entry,
# #     'motortrend': format_motortrend_entry,
# #     'caranddriver': format_caranddriver_entry,
# #     'autoweek': format_autoweek_entry,
# # }
#
