import pprint
import urllib2

from utils import published_parsed_to_datetime
import feedparser as fp
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=2)

def feed(make=None):
    if make is not None:
        return make_feed(make)
    else:
        url = 'http://autoweek.com/rss/2057/feed.xml'
        return parse_feed(url)

def make_feed(make):
    pass


def parse_feed(url, make_feed=False):
    entries = fp.parse(url)['entries'][:10]
    return [format_entry(entry) for entry in entries]


def format_entry(entry, make_feed=False):
    # soup = BeautifulSoup(entry['title'], 'html.parser').text
    # try:
    #     image = soup.find('img').attrs['src']
    # except:
    #     image = None

    # summary = BeautifulSoup(entry['summary'], 'html.parser').text
    try:
        image = get_article_image(entry['link'])
    except:
        image = 'http://placehold.it/1000x1000'

    formatted = {
        'title': entry['title'],
        'author': entry['author'],
        'link': entry['link'],
        'date': published_parsed_to_datetime(entry['published_parsed']),
        'image': image,
        'source': 'Autoweek',
    }
    return formatted


def get_article_image(link):
    soup = BeautifulSoup(urllib2.urlopen(link).read(), 'html.parser')
    return soup.find('meta', attrs={'name': 'image'})['content']


if __name__ == "__main__":
    feed()