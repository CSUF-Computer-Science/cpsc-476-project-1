import base64, os
from flask import Flask, request, jsonify
from .data import db as database, auth
app = Flask(__name__)

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

database.init_app(app)


# this function found here: http://blog.luisrei.com/articles/flaskrest.html
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.headers['X-Original-URI'],
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(409)
def conflict(error=None):
    message = {
        'status': 409,
        'message': 'Error: Conflict at ' + request.headers['X-Original-URI'] +' Code '+ error.message
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
        db.execute("INSERT INTO articles(title, content, author) VALUES(?,?,?);", [request.get_json()['title'], request.get_json()['content'], username])
        db.commit()
        for row in db.execute("SELECT id FROM articles WHERE title=(?) AND author=(?) ORDER BY id DESC;", [request.get_json()['title'], username]):
            if row != None:
                db.commit()
                message = jsonify({
                    "url" : "/articles/"+str(row[0]),
                    "id": row[0]
                })
                message.status_code = 201
                return message
        message = jsonify({"error": "could not post article at this time"})
        message.status_code = 401
        return message

@app.route('/article/<int:article_id>', methods=['GET'])#return 200 else 404
def find_article(article_id):
    if request.method == 'GET':
        db = database.get_db(SERVICE_NAME)
        for row in db.execute("SELECT title, content, author, posted FROM articles where id=(?)", [article_id,]):
            if row != None:
                db.commit()
                message = jsonify({
                    "title" : row[0],
                    "content" : row[1],
                    "author" : row[2],
                    "posted" : row[3]
                })
                message.status_code = 200
                return message
        message = jsonify({"error":"the article you are looking for is not here"})
        message.status_code = 404
        return message

@app.route('/article/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    if request.method == 'DELETE':
        #decoding user authorization
        user = request.headers['Authorization'].strip().split(' ')
        username = base64.b64decode(user[1]).decode().split(':', 1)[0]
        db=database.get_db(SERVICE_NAME)
        for row in db.execute("SELECT id FROM articles WHERE id=(?) AND author=(?);", [article_id, username]):
            if row != None:
                db.execute("DELETE FROM articles WHERE id=(?) AND author=(?)", [article_id, username])
                db.commit()
                message = jsonify({"success":"article deleted"})
                message.status_code=200
                return message
        message = jsonify({"error":"no such article exists"})
        message.status_code=404
        return message


@app.route('/article/edit/<int:article_id>', methods=['POST'])
def edit_article(article_id):
    if request.method == 'POST':
        #decoding user authorization
        user = request.headers['Authorization'].strip().split(' ')
        username = base64.b64decode(user[1]).decode().split(':', 1)[0]
        db = database.get_db(SERVICE_NAME)
        for row in db.execute("SELECT id FROM articles WHERE id=(?) AND author=(?);", [article_id, username]):
            if row != None:
                db.execute("UPDATE articles SET content=(?), posted=CURRENT_TIMESTAMP WHERE id=(?) AND author=(?);", [request.get_json()['content'], article_id, username])
                db.commit()
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
        for row in db.execute("SELECT id, title, content, author, posted FROM articles ORDER BY id DESC LIMIT (?);", [recent_articles,]):
            if row != None:
                collect.append({
                        "url" : "http://localhost/article/"+str(row[0]),
                        "title" : row[1],
                        "content" : row[2],
                        "author" : row[3],
                        "posted" : row[4]
                    })
        message = jsonify({"success":collect})
        message.status_code = 200
        return message

@app.route('/article/meta/<int:recent_articles>', methods=['GET'])
def meta_articles(recent_articles):
    if request.method == 'GET':
            db = database.get_db(SERVICE_NAME)
            collect = list()
            if recent_articles == 0:
                message = jsonify({"error":"not going to attempt to retrieve zero articles"})
                message.status_code = 404
                return message
            for row in db.execute("SELECT id, title, content, author, posted FROM articles ORDER BY id DESC LIMIT (?);", [recent_articles,]):
                if row != None:
                    collect.append({
                            "url" : "<url>http://localhost/article/"+str(row[0])+"</url>",
                            "title" : "<title>"+row[1]+"</title>",
                            "author" : "<author>"+row[3]+"</author>",
                            "posted" : "<pubDate>"+row[4]+"</pubDate>",
                            "comments" : "<comments>http://localhost/article/"+str(row[0])+"/comments</comments>",
                            "category" : "<category>http://localhost/article/"+str(row[0])+"/tags</category>"
                        })
            message = jsonify({"success":collect})
            message.status_code = 200
            return message
