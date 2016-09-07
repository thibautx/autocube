import feeds
from flask import Blueprint, render_template, request

news_module = Blueprint('_news', __name__, url_prefix='/news')

f = {
    'autoblog': feeds.autoblog_feed,
    'motortrend': feeds.motortrend_feed,
    'caranddriver': feeds.caranddriver_feed,
    'thecarconnection': feeds.thecarconnection_feed,
    'autoweek': feeds.autoweek_feed,
    'automobilemag': feeds.automobilemag_feed,
}

@news_module.route('/')
def news():
    return render_template('news/index.html')

@news_module.route('/display', methods=['GET'])
def display():
    if request.method == 'GET':

        news_items = []

        subscriptions = request.args.getlist('feeds')
        for subscription in subscriptions:
            news_items += f[subscription]()

        return render_template('news/index.html', news_items=news_items)