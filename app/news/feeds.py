import pprint
import feedparser as fp
from bs4 import BeautifulSoup

def parse_feed(url):
    entries = fp.parse(url)['entries']
    return [format_entry(entry) for entry in entries]

def format_entry(entry):
    soup = BeautifulSoup(entry['summary'], 'html.parser')
    image = soup.find('img').attrs['src']
    summary = BeautifulSoup(entry['summary'], 'html.parser').text

    formatted = {
        'title': entry['title'],
        'author': entry['author'],
        'link': entry['link'],
        'date': entry['published'],
        'summary': summary,
        'image': image,
    }

    return formatted

def autoblog_feed():
    url = 'http://www.autoblog.com/rss.xml'
    return parse_feed(url)


def motortrend_feed():
    url = 'http://www.motortrend.com/widgetrss/motortrend-stories.xml'
    return parse_feed(url)


def caranddriver_feed():
    url = 'http://feeds.feedburner.com/caranddriver/blog.xml'
    return parse_feed(url)

def topgear_feed():
    pass

def thecarconnection_feed():
    url = 'http://feeds.highgearmedia.com/?sites=TheCarConnection&type=all'
    return parse_feed(url)

def autoweek_feed():
    url = 'http://autoweek.com/rss.xml'
    return parse_feed(url)

def automobilemag_feed():
    url = 'http://www.automobilemag.com/news/feed/'
    return parse_feed(url)

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(autoblog_feed()[0])

