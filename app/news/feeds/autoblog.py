import feedparser as fp
from bs4 import BeautifulSoup

from utils import published_parsed_to_datetime


def feed(make=None):
    if make is not None:
        return make_feed(make)
    else:
        url = 'http://www.autoblog.com/rss.xml'
        return parse_feed(url, make_feed=True)


def make_feed(make):
    url = 'http://www.autoblog.com/category/{}/rss.xml'.format(make)
    return parse_feed(url)


def parse_feed(url, make_feed=False):
    entries = fp.parse(url)['entries'][:10]
    return [format_entry(entry,) for entry in entries]

def format_entry(entry, make_feed=False):
    soup = BeautifulSoup(entry['summary'], 'html.parser')
    try:
        image = soup.find('img').attrs['src']
    except:
        image = None

    summary = BeautifulSoup(entry['summary'], 'html.parser').text
    if make_feed is True:
        summary = summary.split('\n')[2]                # filter out "Filed under"
    else:
        summary = summary.split('\n')[3]                # filter out "Filed under"
    summary = summary.split('Continue reading')[0]      # filter out "Continue reading"

    formatted = {
        'title': entry['title'],
        'author': entry['author'],
        'link': entry['link'],
        'date': published_parsed_to_datetime(entry['published_parsed']),
        'summary': summary,
        'image': image,
        'source': 'Autoblog',
    }

    return formatted

if __name__ == "__main__":
    feed()