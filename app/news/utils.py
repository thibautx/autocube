import json
from collections import OrderedDict

from flask_login import current_user

import feeds
from app import db
from app.garage.models import Car
from app.profile.models import User

f = OrderedDict()
f['Autoblog'] = feeds.autoblog.feed
f['Autoweek'] = feeds.autoweek.feed
# f['Car and Driver'] = feeds.caranddriver.feed

news_categories = sorted(['Safety', 'Reviews'])


def get_user_news_feeds():
    """
    Return the user's news subscriptions

    :return:
    """
    try:
        user_feeds = json.loads(User.query.get(current_user.id).news_subscriptions)
    except:
        db_update_news_subscriptions([])
        user_feeds = json.loads(User.query.get(current_user.id).news_subscriptions)

    return user_feeds


def get_user_news_categories():
    try:
        user_categories = json.loads(User.query.get(current_user.id).news_categories)
    except:
        db_update_news_categories([])
        user_categories = json.loads(User.query.get(current_user.id).news_categories)

    return user_categories


def get_all_news(user_feeds):
    """
    Return all news from user's news subscriptions.

    :return:
    """

    print 'getting all news'
    news_items = []
    for feed, val in user_feeds.items():
        if val == 1:
            try:
                news_items += f[feed]()
            except Exception as e:
                print repr(e)

    # return sorted(news_items, key=lambda x: x['date'])
    return news_items


def get_all_makes_news(user_feeds, makes):
    """
    Get news for all makes.

    :param user_feeds:
    :param makes:
    :return:
    """
    make_feeds = {make: [] for make in makes}
    for make in makes:
        make_feeds[make] = get_make_news(user_feeds, make)

    return make_feeds


def get_make_news(user_feeds, make):
    """
    Get news for one make.

    :param user_feeds:
    :param make: (string)
    :return:
    """
    print 'get make news'
    news_items = []
    for feed, val in user_feeds.items():
        if val == 1:
            try:
                news_items += f[feed](make=make)
            except:
                pass

    return news_items


def get_user_distinct_makes():
    cars_distinct_make = Car.query.filter(Car.user_id == current_user.id).distinct(Car.make).all()  #
    makes = [car.make for car in cars_distinct_make]
    return makes


def initialize_feeds(user_id):
    """
    Initialize all subscriptions to 1

    :param subscriptions:
    """
    subscriptions_json = {}
    for feed in f:
        subscriptions_json[feed] = 1

    user = User.query.get(user_id)
    user.news_subscriptions = json.dumps(subscriptions_json)
    db.session.commit()


def db_update_news_subscriptions(subscribed_feeds):
    """
    Update user's news subscriptions in the database.

    :param subscriptions:
    """
    subscriptions_json = {}
    for feed in f:
        if feed in subscribed_feeds:
            subscriptions_json[feed] = 1
        else:
            subscriptions_json[feed] = 0

    user = User.query.get(current_user.id)
    user.news_subscriptions = json.dumps(subscriptions_json)
    db.session.commit()


def db_update_news_categories(subscribed_categories):
    categories_json = {}
    for category in news_categories:
        if category in subscribed_categories:
            categories_json[category] = 1
        else:
            categories_json[category] = 0

    user = User.query.get(current_user.id)
    user.news_categories = json.dumps(categories_json)
    db.session.commit()


