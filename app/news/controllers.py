import json
from collections import OrderedDict
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.garage.models import Car
from app.profile.models import User

import feeds

news_module = Blueprint('_news', __name__, url_prefix='/news')

f = OrderedDict()
f['autoblog'] = feeds.autoblog.feed
f['autoweek'] = feeds.autoweek.feed
# f['motortrend'] = sadf.motortrend_feed
# f['caranddriver'] = sadf.caranddriver_feed
# f['thecarconnection'] = sadf.thecarconnection_feed
# f['automobilemag'] = sadf.automobilemag_feed

PER_PAGE = 10


@news_module.route('/')
@login_required
def news():
    try:
        user_feeds = json.loads(User.query.get(current_user.id).news_subscriptions)
    except:
        _update_subscriptions([])
        user_feeds = json.loads(User.query.get(current_user.id).news_subscriptions)


    # TODO: multi-sort by date
    # load subscribed sadf
    news_items = []
    for feed, val in user_feeds.items():
        if val == 1:
            try:
                news_items += f[feed]()
            except Exception as e:
                print repr(e)

    print news_items

    make_feeds = get_make_feeds(user_feeds)
    return render_template('news/index.html',
                           feeds=f,
                           news_items=news_items,
                           user_feeds=user_feeds,
                           makes=make_feeds.keys(),
                           make_feeds=make_feeds)


def get_make_feeds(user_feeds):
    cars_distinct_make = Car.query.filter(Car.user_id == current_user.id).distinct(Car.make).all()  #
    makes = [car.make for car in cars_distinct_make]
    make_feeds = {make: [] for make in makes}
    for make in makes:
        for feed, val in user_feeds.items():
            if val == 1:
                try:
                    make_feeds[make] += f[feed](make=make)
                except:
                    pass

    return make_feeds

@news_module.route('/update-subscriptions', methods=['POST'])
@login_required
def update_subscriptions():
    if request.method == 'POST':
        subscriptions = request.form.getlist("feeds")
        _update_subscriptions(subscriptions)

    return redirect(url_for('.news'))


def _update_subscriptions(subscriptions):
    subscriptions_json = {}
    for feed in f:
        if feed in subscriptions:
            subscriptions_json[feed] = 1
        else:
            subscriptions_json[feed] = 0
    user = User.query.get(current_user.id)
    user.news_subscriptions = json.dumps(subscriptions_json)
    db.session.commit()
