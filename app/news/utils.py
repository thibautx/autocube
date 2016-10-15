import json
from collections import OrderedDict
from app.garage.models import Car
from flask_login import current_user
import feeds
from app import db
from app.profile.models import User


f = OrderedDict()
f['Autoblog'] = feeds.autoblog.feed
f['Autoweek'] = feeds.autoweek.feed

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
    news_items = []
    for feed, val in user_feeds.items():
        if val == 1:
            try:
                news_items += f[feed]()
            except Exception as e:
                print repr(e)

    return news_items


def get_makes_news(user_feeds, makes):
    make_feeds = {make: [] for make in makes}
    for make in makes:
        for feed, val in user_feeds.items():
            if val == 1:
                try:
                    make_feeds[make] += f[feed](make=make)
                except:
                    pass

    return make_feeds


def get_user_distinct_makes():
    cars_distinct_make = Car.query.filter(Car.user_id == current_user.id).distinct(Car.make).all()  #
    makes = [car.make for car in cars_distinct_make]
    return makes


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
            categories_json[category] = 1

    user = User.query.get(current_user.id)
    user.news_categories = json.dumps(categories_json)
    db.session.commit()