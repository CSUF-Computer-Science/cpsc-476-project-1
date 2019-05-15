import os, datetime
import requests
from .data.rfeed import Item, Feed
from flask import Flask, jsonify, request as flask_request
from cachecontrol import CacheControlAdapter
from cachecontrol.heuristics import LastModified

app = Flask(__name__)

adapter = CacheControlAdapter(heuristic=LastModified())

sess = requests.Session()
sess.mount('http://', adapter)
sess.mount('https://', adapter)

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

@app.route("/rss/summary", methods=['GET'])
def latest_articles():
    if flask_request.method == 'GET':
        response = sess.get('http://localhost/article/collect/10')
        article_collection = []
        if response.status_code == requests.codes.ok:
            articles = response.json()['success']
            for article in articles:
                article_collection.append(
                    Item(
                        title = article['title'],
                        author= article['author'],
                        pubDate= datetime.datetime.strptime(article['posted'], "%a, %d %b %Y %H:%M:%S %Z"),
                        link = article['url'],
                    )
                )
            feed = Feed(
                title = "New Kids On The Blog RSS Feed",
                link = "http://localhost/rss/summary",
                description = "RSS 2.0 feed generated with rfeed",
                language = "en-US",
                items = article_collection
            )
        return feed.rss()

@app.route("/rss/feed", methods=['GET'])
def feed_articles():
    if flask_request.method == 'GET':
        response = sess.get('http://localhost/article/collect/10')
        article_collection = []
        if response.status_code == requests.codes.ok:
            articles = response.json()['success']
            for article in articles:
                article_id = article['url'].split('/')[-1]
                articleItem = Item(
                    title = article['title'],
                    link = f'http://localhost/article/{article_id}',
                    pubDate = datetime.datetime.strptime(article['posted'], "%a, %d %b %Y %H:%M:%S %Z")
                    )
                response = sess.get(f'http://localhost/article/{article_id}')
                if response.status_code == requests.codes.ok:
                    articleInfo = response.json()
                    articleItem.title = articleInfo['title']
                    articleItem.author = articleInfo['author']
                    articleItem.description = articleInfo['content']
                response = sess.get(f'http://localhost/tags/article/{article_id}')
                if response.status_code == requests.codes.ok:
                    articleItem.categories = response.json()['tags']
                response = sess.get(f'http://localhost/comments/article/{article_id}')
                if response.status_code == requests.codes.ok:
                    articleItem.comments = response.json()['count']
                article_collection.append(articleItem)

        feed = Feed(
            title = "New Kids On The Blog RSS Feed",
            link = f'http://localhost/rss/feed',
            description = "RSS 2.0 feed generated with rfeed",
            language = "en-US",
            items = article_collection
        )
        return feed.rss()

@app.route("/rss/comments", methods=['GET'])
def comment_articles():
    if flask_request.method == 'GET':
        response = sess.get('http://localhost/article/collect/10')
        comment_collection = []
        if response.status_code == requests.codes.ok:
            articles = response.json()['success']
            for article in articles:
                article_id = article['url'].split('/')[-1]
                response = sess.get(f'http://localhost/comments/100/article/{article_id}')
                if response.status_code == requests.codes.ok:
                    comments = response.json()['comments']
                    for comment in comments:
                        commentItem = Item(
                            title = comment['author'],
                            description = comment['content'],
                            pubDate = datetime.datetime.strptime(comment['posted'], "%a, %d %b %Y %H:%M:%S %Z"),
                            link = f'http://localhost/article/{article_id}'
                        )
                        comment_collection.append(commentItem)

            feed = Feed(
            title = "New Kids On The Blog RSS Feed",
            link = f'http://localhost/rss/summary',
            description = "RSS 2.0 feed generated with rfeed",
            language = "en-US",
            items = comment_collection
        )
    return feed.rss()
