import sys, os
from flask import Flask, jsonify, request
from .data import db, auth

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

app = Flask(__name__, instance_relative_config=True)
app.config["DEBUG"] = True
db.init_app(app)

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

@app.errorhandler(409)
def conflict(error=None):
    message = {
        'status': 409,
        'message': 'Error: Conflict at ' + request.headers.get('X-Original-URI', request.path) +' Code '+ str(error) + error.message
    }
    resp = jsonify(message)
    resp.status_code = 409
    return resp

#get all articles connected to a tag
@app.route('/tags/<name>', methods=['GET'])
def getArticles(name):
    mydb = db.get_db(SERVICE_NAME)
    try:
        results = list(mydb.execute("SELECT article,name FROM tags"))
        results = list(filter(lambda row: row[1] == name, results))
    except:
            e=sys.exc_info()[0]
            return conflict(e)        
    if results:
        resultsOut = {'count': len(results),
                      'articles': []}
        for t in results:
            resultsOut['articles'].append(f"/article/{t[0]}")
        resp = jsonify(resultsOut)
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/tags/article/<uuid:id>', methods = ['POST', 'DELETE'])
def tags(id):

    if request.method == 'POST':
        mydb = db.get_db(SERVICE_NAME)
        content = request.get_json()
        tagnames = content.get('TagNames'), None
        if tagnames == None:
            resp = jsonify({"error": "Error: Missing Arguments. Please specify TagName(s) to add."})
            resp.status_code = 400
            return resp
        else:
            for t in tagnames[0]:
                try:
                    mydb.execute(mydb.prepare('INSERT INTO tags(name, article) VALUES (?,?)'), [t, id])
                except:
                    e=sys.exc_info()[0]
                    return conflict(e)
            try:
                tags = list(mydb.execute(mydb.prepare("SELECT name FROM tags WHERE article=?;"), [id]))
            except:
                e=sys.exc_info()[0]
                return conflict(e)    
            article_id = "/article/"+str(id)
            location = article_id + "/tags/"
            results = {'article_id': article_id,
                       'tags': []}
            for t in tags:
                results['tags'].append(t[0])
            resp = jsonify(results)
            resp.status_code = 200
            resp.headers['Location']=location
            return resp
    #delete 1 or more tags from an article
    elif request.method == 'DELETE':
        mydb = db.get_db(SERVICE_NAME)
        content = request.get_json()
        tagnames = content.get('TagNames'), None
        if tagnames == None:
            resp = jsonify({"error": "Error: Missing Arguments. Please specify TagName(s) to add."})
            resp.status_code = 400
            return resp
        else:
            for t in tagnames[0]:
                try:
                    mydb.execute(mydb.prepare('DELETE FROM tags WHERE article=? AND name=?'), [id, t])
                except:
                    e=sys.exc_info()[0]
                    return conflict(e)
            try:
                tags = list(mydb.execute(mydb.prepare("SELECT name FROM tags WHERE article=?"), [id]))
            except:
                e=sys.exc_info()[0]
                return conflict(e)
            article_id = "/article/"+str(id)
            results = {'article_id': article_id,
                       'tags': []}
            for t in tags:
                results['tags'].append(t[0])
            resp = jsonify(results)
            resp.status_code = 200
            return resp
    else:
        resp = jsonify({'message': request.url + " contains no such method.",
                    'status':405})
        return resp

@app.route('/tags/all/article/<uuid:id>', methods = ['GET'])
def getTags(id):
        #get all tags connected to an article
    if request.method == 'GET':
        mydb = db.get_db(SERVICE_NAME)
        try:
            results = list(mydb.execute(mydb.prepare("SELECT name FROM tags WHERE article=?"), [id]))
        except:
            e=sys.exc_info()[0]
            return conflict(e)
        if results:
            resultsOut = {'article_id': f"/article/{id}",
                          'tags': []}
            for t in results:
                resultsOut['tags'].append(t[0])
            resp = jsonify(resultsOut)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    else:
        resp = jsonify({'message': request.url + " contains no such method.",
                    'status':405})
        return resp