from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

import utils

news_module = Blueprint('_news', __name__, url_prefix='/news')

# f['motortrend'] = sadf.motortrend_feed
# f['caranddriver'] = sadf.caranddriver_feed
# f['thecarconnection'] = sadf.thecarconnection_feed
# f['automobilemag'] = sadf.automobilemag_feed


PER_PAGE = 10


@login_required
@news_module.route('/')
def news():

    user_feeds = utils.get_user_news_feeds()
    user_categories = utils.get_user_news_categories()

    all_news = utils.get_all_news(user_feeds)
    makes = utils.get_user_distinct_makes()
    make_news = utils.get_makes_news(user_feeds, makes)

    return render_template('news/news_grid.html',
                           feeds=utils.f,
                           user_feeds=user_feeds,
                           news_categories=utils.news_categories,
                           user_categories=user_categories,
                           news_items=all_news,
                           makes=makes,
                           make_feeds=make_news)


@news_module.route('/update-subscriptions', methods=['POST'])
@login_required
def update_subscriptions():
    if request.method == 'POST':
        subscriptions = request.form.getlist('feeds')
        utils.db_update_news_subscriptions(subscriptions)

    return redirect(url_for('.news'))


