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
        url = 'http://feeds.feedburner.com/caranddriver/blog'
        return parse_feed(url)

def make_feed(make):
    pass


def parse_feed(url, make_feed=False):
    entries = fp.parse(url)['entries'][:10]
    return [format_entry(entry) for entry in entries]


def format_entry(entry, make_feed=False):
    try:
        markup = entry['content'][0]['value']
        soup = BeautifulSoup(markup, 'html.parser')
        image = soup.find('img', attrs={'height': '383'})['src']
    except:
        image = 'http://placehold.it/1000x1000'

    formatted = {
        'title': entry['title'],
        'author': entry['author'],
        'link': entry['link'],
        'date': published_parsed_to_datetime(entry['published_parsed']),
        'image': image,
        'source': 'Car and Driver',
    }
    return formatted


def get_article_image(link):
    # soup = BeautifulSoup(urllib2.urlopen(link).read(), 'html.parser')
    # img = soup.find('img', attrs={'class': 'resp-img embedded-image--image'})['data-default']
    # img.replate('429x262', )
    # return
    pass

if __name__ == "__main__":
    feed()