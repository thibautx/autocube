import json
import feeds
import app
from app import db
from app.profile.models import User
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from collections import OrderedDict
from flask_paginate import Pagination

news_module = Blueprint('_news', __name__, url_prefix='/news')

f = OrderedDict()
f['autoblog'] = feeds.autoblog_feed
f['motortrend'] = feeds.motortrend_feed
f['caranddriver'] = feeds.caranddriver_feed
f['thecarconnection'] = feeds.thecarconnection_feed
f['autoweek'] = feeds.autoweek_feed
f['automobilemag'] = feeds.automobilemag_feed

PER_PAGE = 10

@news_module.route('/', defaults={'page': 1})
@news_module.route('/<int:page>')
@login_required
def news(page):
    user_feeds = json.loads(User.query.get(current_user.id).news_subscriptions)

    # TODO: multi-sort by date
    # load subscribed feeds
    news_items = []
    for feed, val in user_feeds.items():
        if val == 1:
            news_items += f[feed]()

    i = (page-1)*PER_PAGE
    news_items_display = news_items[i:i+5]
    pagination = Pagination(page=page, total=len(news_items), per_page=10)

    return render_template('news/index.html',
                           pagination=pagination,
                           feeds=f,
                           user_feeds=user_feeds,
                           news_items=news_items_display)


@news_module.route('/update-subscriptions', methods=['POST'])
@login_required
def update_subscriptions():
    if request.method == 'POST':
        subscriptions = request.form.getlist("feeds")
        subscriptions_json = {}
        for feed in f:
            if feed in subscriptions:
                subscriptions_json[feed] = 1
            else:
                subscriptions_json[feed] = 0
        user = User.query.get(current_user.id)
        user.news_subscriptions = json.dumps(subscriptions_json)
        db.session.commit()
    return redirect(url_for('.news'))

# @news_module.route('/display', methods=['GET'])
# @login_required
# def display():
#     if request.method == 'GET':
#         news_items = []
#         subscriptions = request.args.getlist('feeds')
#         for subscription in subscriptions:
#             news_items += f[subscription]()
#         return render_template('news/index.html', news_items=news_items)
#
