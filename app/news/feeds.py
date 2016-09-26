import re
import pprint
import feedparser as fp
from bs4 import BeautifulSoup


def parse_feed(url, blog, make_feed=False):
    entries = fp.parse(url)['entries']
    f_format = formatters[blog]
    return [f_format(entry, make_feed=make_feed) for entry in entries]


def format_entry(entry):
    soup = BeautifulSoup(entry['summary'], 'html.parser')
    try:
        image = soup.find('img').attrs['src']
    except:
        image = None

    summary = BeautifulSoup(entry['summary'], 'html.parser').text

    formatted = {
        'title': entry['title'],
        'author': entry['author'],
        'link': entry['link'],
        'date': entry['published'],
        'summary': summary,
        'image': image,
    }

    # return formatted


def autoblog_feed(make=None):
    if make is not None:
        return autoblog_make_feed(make)
    else:
        url = 'http://www.autoblog.com/rss.xml'
        return parse_feed(url, 'autoblog', make_feed=True)


def autoblog_make_feed(make):
    url = 'http://www.autoblog.com/category/{}/rss.xml'.format(make)
    return parse_feed(url, 'autoblog')


def format_autoblog_entry(entry, make_feed=False):
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
        'date': entry['published'],
        'summary': summary,
        'image': image,
    }

    return formatted


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


formatters = {
    'autoblog': format_autoblog_entry,
}

