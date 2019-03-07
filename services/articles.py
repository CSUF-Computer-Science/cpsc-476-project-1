import sys, base64, sqlite3
from flask import Flask, request, g, jsonify, Response
from data import db as database, auth
app = Flask(__name__)

database.init_app(app)
basic_auth = auth.GetAuth()
basic_auth.init_app(app)

@app.route('/article/new', methods=['POST'])#return 201 with URL in header
@basic_auth.required
def new_article():
    if request.method == 'POST':
        #decoding user authorization
        user = request.headers['Authorization'].strip().split(' ')
        username, password = base64.b64decode(user[1]).decode().split(':', 1)
        db = database.get_db()   
        db.execute("INSERT INTO articles(title, content, author) VALUES(?,?,?);", [request.get_json()['title'], request.get_json()['content'], username])
        db.commit()
        for row in db.execute("SELECT id FROM articles WHERE title=(?) AND author=(?) ORDER BY id DESC;", [request.get_json()['title'], username]):
            if row != None:
                db.commit()
                database.close_db()
                message = jsonify({"URL" : "http://localhost:5001/articles/"+str(row[0])})
                message.status_code = 201
                return message
        message = jsonify({"error": "could not post article at this time"})
        message.status_code = 401
        return message

@app.route('/article/<int:article_id>', methods=['GET'])#return 200 else 404
def find_article(article_id):
    if request.method == 'GET':
        db = database.get_db()
        for row in db.execute("SELECT title, content, author, posted FROM articles where id=(?)", [article_id,]):
            if row != None:
                db.commit()
                database.close_db()
                message = jsonify({
                    "title" : row[0],
                    "content" : row[1],
                    "author" : row[2],
                    "posted" : row[3]
                })
                message.status_code = 200
                return message
        database.close_db()
        message = jsonify({"error":"the article you are looking for is not here"})
        message.status_code = 404
        return message

@app.route('/article/delete/<int:article_id>', methods=['DELETE']) #200 and 404
@basic_auth.required
def delete_article(article_id):
    if request.method == 'DELETE':
        #decoding user authorization
        user = request.headers['Authorization'].strip().split(' ')
        username, password = base64.b64decode(user[1]).decode().split(':', 1)
        db=database.get_db()
        for row in db.execute("SELECT id FROM articles WHERE id=(?) AND author=(?);", [article_id, username]):
            if row != None:
                db.execute("DELETE FROM articles WHERE id=(?) AND author=(?)", [article_id, username])
                db.commit()
                database.close_db()
                message = jsonify({"success":"article deleted"})
                message.status_code=200
                return message
        database.close_db()
        message = jsonify({"error":"no such article exists"})
        message.status_code=404
        return message


@app.route('/article/edit/<int:article_id>', methods=['POST'])#return 200 or 404
@basic_auth.required
def edit_article(article_id):
    if request.method == 'POST':
        #decoding user authorization
        user = request.headers['Authorization'].strip().split(' ')
        username, password = base64.b64decode(user[1]).decode().split(':', 1)
        db = database.get_db()
        for row in db.execute("SELECT id FROM articles WHERE id=(?) AND author=(?);", [article_id, username]):
            if row != None:
                db.execute("UPDATE articles SET content=(?), posted=CURRENT_TIMESTAMP WHERE id=(?) AND author=(?);", [request.get_json()['content'], article_id, username])
                db.commit()
                database.close_db()
                message = jsonify({"success":"content updated"})
                message.status_code=200
                return message
        message = jsonify({"error":"could not update content"})
        message.status_code=404
        return message

@app.route('/article/collect/<int:recent_articles>', methods=['GET'])#return 200 or 404
def collect_article(recent_articles):
    if request.method == 'GET':
        db = database.get_db()
        print(recent_articles)
        collect = list()
        for row in db.execute("SELECT id, title, content, author, posted FROM articles ORDER BY id DESC LIMIT (?);", [recent_articles,]):
            if row != None:
                print(type(row[4]))
                collect.append({
                        "URL" : "https://127.0.0.1:5001/articles/"+str(row[0]),
                        "title" : row[1],
                        "content" : row[2],
                        "author" : row[3],
                        "posted" : row[4]
                    })
            else:
                message = jsonify({"error":"could not find articles"})
                message.status_code = 404
                return message
        message = jsonify({"success":collect})
        message.status_code = 200
        return message


if __name__ == '__main__':
     app.run("127.0.0.1", "5001")