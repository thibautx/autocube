import re
import pprint
import feedparser as fp
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=2)

def parse_feed(url, source, make_feed=False):
    entries = fp.parse(url)['entries']
    # f_format = formatters[blog]
    return [format_entry(entry, source) for entry in entries]
    # return [f_format(entry, make_feed=make_feed) for entry in entries]


def format_entry(entry, source):
    soup = BeautifulSoup(entry['summary'], 'html.parser')
    try:
        image = soup.find('img').attrs['src']
    except:
        image = None

    summary = BeautifulSoup(entry['summary'], 'html.parser').text

    formatted = {
        'source': source,
        'title': entry['title'],
        'author': entry['author'],
        'link': entry['link'],
        'date': entry['published'],
        'summary': summary,
        'image': image,
    }
    return formatted

# AUTOBLOG
def autoblog_feed(make=None):
    if make is not None:
        return autoblog_make_feed(make)
    else:
        url = 'http://www.autoblog.com/rss.xml'
        return parse_feed(url, 'Autoblog', make_feed=True)


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


# MOTORTREND
def motortrend_feed(make=None):
    url = 'http://www.motortrend.com/widgetrss/motortrend-stories.xml'
    return parse_feed(url, source='motortrend')


def motortrend_make_feed(make):
    pass


def format_motortrend_entry(entry, make_feed=False):
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

    return formatted


# CAR AND DRIVER (doesn't work?? no rss feed)
def caranddriver_feed(make=None):
    url = 'http://feeds.feedburner.com/caranddriver/blog.xml'
    return parse_feed(url, 'caranddriver')


def format_caranddriver_entry(entry):
    soup = BeautifulSoup(entry['summary'], 'html.parser')
    try:
        image = soup.find('img').attrs['src']
    except:
        image = None

    summary = BeautifulSoup(entry['summary'], 'html.parser').text
    print summary

    formatted = {
        'title': entry['title'],
        'author': entry['author'],
        'link': entry['link'],
        'date': entry['published'],
        'summary': summary,
        'image': image,
    }

    return formatted


# TOPGEAR (doesn't work?? no rss feed)
def topgear_feed():
    pass


def thecarconnection_feed():
    url = 'http://feeds.highgearmedia.com/?sites=TheCarConnection&type=all'
    return parse_feed(url)


# AUTOWEEK
def autoweek_feed(make=None):
    url = 'http://autoweek.com/rss/2057/feed.xml'
    return parse_feed(url, source='autoweek')


def format_autoweek_entry(entry, make_feed=False):
    pp.pprint(entry)
    soup = BeautifulSoup(entry['summary_detail'], 'html.parser').text
    # pp.pprint(soup.text)
    # try:
    #     image = soup.find('img').attrs['src']
    # except:
    #     image = None

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


def automobilemag_feed():
    url = 'http://www.automobilemag.com/news/feed/'
    return parse_feed(url)


formatters = {
    'autoblog': format_autoblog_entry,
    'motortrend': format_motortrend_entry,
    'caranddriver': format_caranddriver_entry,
    'autoweek': format_autoweek_entry,
}

