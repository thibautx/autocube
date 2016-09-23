import json
import feeds
from app import db
from app.profile.models import User
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from collections import OrderedDict

news_module = Blueprint('_news', __name__, url_prefix='/news')

f = OrderedDict()
f['autoblog'] = feeds.autoblog_feed
f['motortrend'] = feeds.motortrend_feed
f['caranddriver'] = feeds.caranddriver_feed
f['thecarconnection'] = feeds.thecarconnection_feed
f['autoweek'] = feeds.autoweek_feed
f['automobilemag'] = feeds.automobilemag_feed

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
    # load subscribed feeds
    news_items = []
    for feed, val in user_feeds.items():
        if val == 1:
            news_items += f[feed]()

    return render_template('news/index.html',
                           feeds=f,
                           news_items=news_items,
                           user_feeds=user_feeds)


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
