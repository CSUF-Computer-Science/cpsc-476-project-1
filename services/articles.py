import base64, os, uuid
from flask import Flask, request, jsonify
from .data import db as database, auth
from werkzeug.http import http_date
from werkzeug.routing import HTTPException

app = Flask(__name__)

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

database.init_app(app)

# this function found here: http://blog.luisrei.com/articles/flaskrest.html
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.headers.get('X-Original-URI', request.path),
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

class NotModified(HTTPException):
    code = 304
    message = 'Not Modified.'

def not_modified(error=None):
    message = {
        'status': 304,
        'message': 'Not Modified.',
    }
    resp = jsonify(message)
    resp.status_code = 304
    return resp

app.register_error_handler(NotModified, not_modified)

@app.errorhandler(409)
def conflict(error=None):
    message = {
        'status': 409,
        'message': 'Error: Conflict at ' + request.headers.get('X-Original-URI', request.path) +' Code '+ error.message
    }
    resp = jsonify(message)
    resp.status_code = 409
    return resp
    
@app.route('/article/new', methods=['POST'])
def new_article():
    if request.method == 'POST':
        #decoding user authorization
        user = request.headers['Authorization'].strip().split(' ')
        username = base64.b64decode(user[1]).decode().split(':', 1)[0]
        db = database.get_db(SERVICE_NAME)
        
        postId = uuid.uuid1()
        try:
            db.execute(db.prepare("INSERT INTO articles(id, posted, title, content, author) VALUES(?, toTimestamp(now()), ?,?,?);"), [postId, request.get_json()['title'], request.get_json()['content'], username])
        except Exception as e:        
            message = jsonify({"error": str(e)})
            message.status_code = 401
            return message

        message = jsonify({
            "url" : "/article/"+str(postId),
            "id": str(postId)
        })
        message.status_code = 201
        return message

@app.route('/article/<uuid:article_id>', methods=['GET'])#return 200 else 404
def find_article(article_id):
    if request.method == 'GET':
        db = database.get_db(SERVICE_NAME)
        results=list(db.execute(db.prepare("SELECT title, content, author, posted FROM articles where id=?"), [article_id,]))

        if len(results) > 0:
            last_modified=http_date(results[0][3])

            if 'If-Modified-Since' in request.headers:
                if last_modified == request.headers['If-Modified-Since']:
                    return not_modified()

            for row in results:
                message = jsonify({
                    "title" : row[0],
                    "content" : row[1],
                    "author" : row[2],
                    "posted" : row[3]
                })
                message.status_code = 200
                message.headers['Last-Modified']=last_modified
                return message
        else:
            return not_found()

@app.route('/article/delete/<uuid:article_id>', methods=['DELETE'])
def delete_article(article_id):
    if request.method == 'DELETE':
        db=database.get_db(SERVICE_NAME)
        results = list(db.execute(db.prepare("SELECT id FROM articles WHERE id=? AND author=?;"), [article_id, auth.getUser()]))
        if len(results) > 0:
            db.execute(db.prepare("DELETE FROM articles WHERE id=?;"), [article_id])
            message = jsonify({"success":"article deleted"})
            message.status_code=200
            return message
        else:
            message = jsonify({"error":"no such article exists"})
            message.status_code=404
            return message


@app.route('/article/edit/<uuid:article_id>', methods=['POST'])
def edit_article(article_id):
    if request.method == 'POST':
        #decoding user authorization
        user = request.headers['Authorization'].strip().split(' ')
        username = base64.b64decode(user[1]).decode().split(':', 1)[0]
        db = database.get_db(SERVICE_NAME)
        for row in db.execute(db.prepare("SELECT id FROM articles WHERE id=? AND author=?;"), [article_id, username]):
            if row != None:
                db.execute(db.prepare("UPDATE articles SET content=?, posted=CURRENT_TIMESTAMP WHERE id=? AND author=?;"), [request.get_json()['content'], article_id, username])
                message = jsonify({"success":"content updated"})
                message.status_code=200
                return message
        message = jsonify({"error":"could not update content"})
        message.status_code=404
        return message

@app.route('/article/collect/<int:recent_articles>', methods=['GET'])
def collect_article(recent_articles):
    if request.method == 'GET':
        db = database.get_db(SERVICE_NAME)
        collect = list()
        if recent_articles == 0:
            message = jsonify({"error":"not going to attempt to retrieve zero articles"})
            message.status_code = 404
            return message
        else:
            articles = list(db.execute("SELECT id, title, content, author, posted FROM articles"))
            articles.sort(key=lambda post: post.posted, reverse=True)
            
            if len (articles) > 0:
                last_modified=http_date(articles[0][4])

                if 'If-Modified-Since' in request.headers:
                    if last_modified == request.headers['If-Modified-Since']:
                        return not_modified()

                for row in articles[0:recent_articles]:
                    collect.append({
                        "url" : "/article/"+str(row[0]),
                        "title" : row[1],
                        "content" : row[2],
                        "author" : row[3],
                        "posted" : row[4]
                    })
                message = jsonify({"success":collect})
                message.status_code = 200
                message.headers['Last-Modified']=last_modified
                return message
            else:
                return not_found()

@app.route('/article/meta/<int:recent_articles>', methods=['GET'])
def meta_articles(recent_articles):
    if request.method == 'GET':
        db = database.get_db(SERVICE_NAME)
        collect = list()
        if recent_articles == 0:
            message = jsonify({"error":"not going to attempt to retrieve zero articles"})
            message.status_code = 404
            return message
        else:
            articles = list(db.execute("SELECT id, title, content, author, posted FROM articles"))
            
            if len(articles) > 0:
                last_modified=http_date(articles[0][4])

                if 'If-Modified-Since' in request.headers:
                    if last_modified == request.headers['If-Modified-Since']:
                        return not_modified()
                
                for row in articles[0:recent_articles]:
                    collect.append({
                        "url" : "<url>http://localhost/article/"+str(row[0])+"</url>",
                        "title" : "<title>"+row[1]+"</title>",
                        "author" : "<author>"+row[3]+"</author>",
                        "posted" : "<pubDate>"+str(row[4])+"</pubDate>",
                        "comments" : "<comments>http://localhost/article/"+str(row[0])+"/comments</comments>",
                        "category" : "<category>http://localhost/article/"+str(row[0])+"/tags</category>"
                    })
                message = jsonify({"success":collect})
                message.status_code = 200
                message.headers['Last-Modified']=last_modified
                return message
            else:
                return not_found()