import os, datetime
import requests
from .data.rfeed import Item, Feed
from flask import Flask, jsonify, request as flask_request
app = Flask(__name__)

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

@app.route("/rss/latest", methods=['GET'])
def latest_articles():
    if flask_request.method == 'GET':
        response = requests.get('http://localhost:5101/article/collect/10')
        article_collection = []
        if response.status_code == requests.codes.ok:
            articles = response.json()['success']
            for article in articles:
                article_collection.append(
                    Item(
                        title = article['title'],
                        author= article['author'],
                        pubDate= datetime.datetime.strptime(article['posted'], "%Y-%m-%d %H:%M:%S"),
                        link = article['url'],
                    )
                )
            feed = Feed(
                title = "New Kids On The Blog RSS Feed",
                link = "https://127.0.0.1:5400/rss/latest",
                description = "RSS 2.0 feed generated with rfeed",
                language = "en-US",
                items = article_collection
            )
        return feed.rss()
        
@app.route("/rss/<int:article_id>/feed", methods=['GET'])
def feed_articles(article_id):
    if flask_request.method == 'GET':
        response = requests.get(f'http://127.0.0.1:5100/article/{article_id}')
        article = Item
        if response.status_code == requests.codes.ok:
            articleInfo = response.json()
            article = Item(
                title = articleInfo['title'],
                author = articleInfo['author'],
                description = articleInfo['content'],
                pubDate= datetime.datetime.strptime(articleInfo['posted'], "%Y-%m-%d %H:%M:%S")
            )
        response = requests.get(f'http://127.0.0.1:5200/article/{article_id}/tags')
        if response.status_code == requests.codes.ok:
            article.categories = response.json()['tags']
        response = requests.get(f'http://127.0.0.1:5300/article/{article_id}/comments')
        if response.status_code == requests.codes.ok:
            article.comments = response.json()['count']
        feed = Feed(
            title = "New Kids On The Blog RSS Feed",
            link = f'http://127.0.0.1:5100/article/{article_id}',
            description = "RSS 2.0 feed generated with rfeed",
            language = "en-US",
            items = [article]
        )
    return feed.rss()

@app.route("/rss/<int:article_id>/comments", methods=['GET'])
def comment_articles(article_id):
    if flask_request.method == 'GET':
        print("A comment feed for each article.")

    return {'default':'the fault'}