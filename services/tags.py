import sqlite3
import click
from flask import g, Flask, Response, jsonify, request
from .data import db
app = Flask(__name__, instance_relative_config=True)
app.config["DEBUG"] = True
db.init_app(app)

# this function found here: http://blog.luisrei.com/articles/flaskrest.html
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

#get all articles connected to a tag
@app.route('tags/<name>', methods=['GET'])
def getArticles(name):
    mydb = db.get_db()
    results = mydb.execute(
            "SELECT * FROM tags WHERE name=?", [name]).fetchall()
    if results:
        resp = jsonify(results)
        resp.status_code = 200
        db.close_db()
        return resp
    else:
        db.close_db()
        return not_found()

@app.route('articles/<id>/tags/', methods = ['GET', 'POST', 'DELETE'])
def tags(id):
    #get all tags connected to an article
    if request.method == 'GET':
        mydb = db.get_db()
        results = mydb.execute(
            "SELECT * FROM tags WHERE article=?", [id]).fetchall()
        if results:
            resp = jsonify(results)
            resp.status_code = 200
            db.close_db()
            return resp
        else:
            db.close_db()
            return not_found()

    #post 1 or more tags to an article
    if request.method == 'POST':
        mydb = db.get_db()
        content = request.get_json()
        tagnames = content.get('TagNames'), None
        if tagnames == None:
            resp = jsonify({"error": "Error: Missing Arguments. Please specify TagName(s) to add."})
            resp.status_code = 400
            return resp
        else:
            for t in tagnames:
                mydb.execute(
                'INSERT INTO tags(name, article)''VALUES (?,?)', [id, t])
            mydb.commit()
            tags = mydb.execute(
                "SELECT name FROM tags WHERE article=?", [id]).fetchall()
            mydb.commit()
            db.close_db()
            article_id = "/articles/"+id
            location = article_id + "/tags/"
            results = {'article_id': article_id,
                       'tags': []}
            for t in tags:
                results['tags'].append(t)
            resp = jsonify(results)
            resp.status_code = 401
            resp.headers['Location']=location
            return resp

    #delete 1 or more tags from an article
    elif request.method == 'DELETE':
        mydb = db.get_db()
        content = request.get_json()
        tagnames = content.get('TagNames'), None
        if tagnames == None:
            resp = jsonify({"error": "Error: Missing Arguments. Please specify TagName(s) to add."})
            resp.status_code = 400
            return resp
        else:
            for t in tagnames:
                mydb.execute('DELETE FROM tags WHERE name=? AND article=?', [t, id])
            mydb.commit()
            tags = mydb.execute(
                "SELECT name FROM tags WHERE article=?", [id]).fetchall()
            db.close_db()
            article_id = "/articles/"+id
            results = {'article_id': article_id,
                       'tags': []}
            for t in tags:
                results['tags'].append(t)
            resp = jsonify(results)
            resp.status_code = 200
            return resp
    else:
        message: {'message': request.url + " contains no such method.",
                  'status': 405}
        resp = jsonify(message)
        resp.status_code = 405
        return resp
