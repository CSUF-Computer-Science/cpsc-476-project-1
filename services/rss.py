import os, datetime
import requests
from data.rfeed import Item, Feed
from flask import Flask, jsonify, request as flask_request
app = Flask(__name__)

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

@app.route("/rss/latest", methods=['GET'])
def latest_articles():
    if flask_request.method == 'GET':
        response = requests.get('http://localhost:5000/article/collect/10')
        article_collection = []
        if response.json()['success']:
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
                link = "https://127.0.0.1:600/rss/latest",
                description = "RSS 2.0 feed generated with rfeed",
                language = "en-US",
                items = article_collection
            )
        return feed.rss()
@app.route("/rss/feed", methods=['GET'])
def feed_articles():
    if flask_request.method == 'GET':
        print("A full feed containing the full text for each article, its tags as RSS categories, and a comment count.")

    return {'default':'the fault'}

@app.route("/rss/<int:article_id>/comments", methods=['GET'])
def feed_articles():
    if flask_request.method == 'GET':
        print("A comment feed for each article.")

    return {'default':'the fault'}