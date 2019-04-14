import os, datetime
import requests
from .data.rfeed import Item, Feed
from flask import Flask, jsonify, request as flask_request
app = Flask(__name__)

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

@app.route("/rss/summary", methods=['GET'])
def latest_articles():
    if flask_request.method == 'GET':
        response = requests.get('http://localhost:5000/article/collect/10')
        article_collection = []
        if response.status_code == requests.codes.ok:
            articles = response.json()['success']
            for article in articles:
                article_collection.append(
                    Item(
                        title = article['title'],
                        author= article['author'],
                        pubDate= datetime.datetime.strptime(article['posted'], "%Y-%m-%d %H:%M:%S.%f"),
                        link = article['url'],
                    )
                )
            feed = Feed(
                title = "New Kids On The Blog RSS Feed",
                link = "https://127.0.0.1:5400/rss/summary",
                description = "RSS 2.0 feed generated with rfeed",
                language = "en-US",
                items = article_collection
            )
        return feed.rss()
        
@app.route("/rss/feed", methods=['GET'])
def feed_articles():
    if flask_request.method == 'GET':
        response = requests.get('http://localhost:5000/article/collect/10')
        article_collection = []
        if response.status_code == requests.codes.ok:
            articles = response.json()['success']
            for article in articles:
                article_id = article['url'].split('/')[-1]
                articleItem = Item(
                    title = article['title'],
                    link = f'https://localhost:5100/article/{article_id}',
                    pubDate = datetime.datetime.strptime(article['posted'], "%Y-%m-%d %H:%M:%S.%f")
                    )
                response = requests.get(f'http://localhost:5000/article/{article_id}')
                if response.status_code == requests.codes.ok:
                    articleInfo = response.json()
                    articleItem.title = articleInfo['title'],
                    articleItem.author = articleInfo['author'],
                    articleItem.description = articleInfo['content']
                response = requests.get(f'http://localhost:5100/article/{article_id}/tags')
                if response.status_code == requests.codes.ok:
                    articleItem.categories = response.json()['tags']
                response = requests.get(f'http://localhost:5200/article/{article_id}/comments')
                if response.status_code == requests.codes.ok:
                    articleItem.comments = response.json()['count']
                article_collection.append(articleItem)

        feed = Feed(
            title = "New Kids On The Blog RSS Feed",
            link = f'http://localhost:5000/rss/feed',
            description = "RSS 2.0 feed generated with rfeed",
            language = "en-US",
            items = article_collection
        )
        return feed.rss()

@app.route("/rss/comments", methods=['GET'])
def comment_articles():
    if flask_request.method == 'GET':
        response = requests.get('http://localhost:5000/article/collect/10')
        comment_collection = []
        if response.status_code == requests.codes.ok:
            articles = response.json()['success']
            for article in articles:
                article_id = article['url'].split('/')[-1]
                response = requests.get(f'http://localhost:5200/article/{article_id}/comments/100')
                if response.status_code == requests.codes.ok:
                    comments = response.json()['comments']
                    for comment in comments:
                        commentItem = Item(
                            title = comment['author'],
                            description = comment['content'],
                            pubDate = datetime.datetime.strptime(comment['posted'], "%Y-%m-%d %H:%M:%S.%f"),
                            link = f'http://localhost:5000/article/{article_id}'
                        )
                        comment_collection.append(commentItem)

            feed = Feed(
            title = "New Kids On The Blog RSS Feed",
            link = f'http://localhost:5000/rss/summary',
            description = "RSS 2.0 feed generated with rfeed",
            language = "en-US",
            items = comment_collection
        )
    return feed.rss()