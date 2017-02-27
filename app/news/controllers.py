from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

import utils

news_module = Blueprint('_news', __name__, url_prefix='/news')


PER_PAGE = 10

@news_module.route('/')
@login_required
def news():
    """
    Homepage (All News)

    :return:
    """

    user_feeds = utils.get_user_news_feeds()
    user_categories = utils.get_user_news_categories()
    all_news = utils.get_all_news(user_feeds)
    makes = utils.get_user_distinct_makes()

    return render_template('news/news.html',
                           user_feeds=user_feeds,
                           news_categories=utils.news_categories,
                           user_categories=user_categories,
                           news_items=all_news,
                           makes=makes,
                           make_feeds=make_news,
                           active='all')


@news_module.route('/<make>')
@login_required
def make_news(make):
    user_feeds = utils.get_user_news_feeds()
    user_categories = utils.get_user_news_categories()
    makes = utils.get_user_distinct_makes()
    news_items = utils.get_make_news(user_feeds, make)

    return render_template('news/news.html',
                           user_feeds=user_feeds,
                           news_categories=utils.news_categories,
                           user_categories=user_categories,
                           news_items=news_items,
                           makes=makes,
                           make_feeds=make_news,
                           active=make)


@news_module.route('/subscriptions')
@login_required
def subscriptions():
    """
    User's subscriptions (feeds & categories)

    :return:
    """

    user_categories = utils.get_user_news_categories()
    user_feeds = utils.get_user_news_feeds()
    makes = utils.get_user_distinct_makes()

    return render_template('news/subscriptions_form.html',
                           user_feeds=user_feeds,
                           news_categories=utils.news_categories,
                           user_categories=user_categories,
                           makes=makes,
                           feeds=utils.f,
                           active='subscriptions')


@news_module.route('/update-subscriptions', methods=['POST'])
@login_required
def update_subscriptions():
    if request.method == 'POST':
        subscriptions = request.form.getlist('feeds')
        utils.db_update_news_subscriptions(subscriptions)

    return redirect(url_for('.news'))


