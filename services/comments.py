import sys, os, uuid, cassandra
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
        'message': 'Error: Conflict at ' + request.get('X-Original-URI', request.path) +' Code '+ str(error)
    }
    resp = jsonify(message)
    resp.status_code = 409
    return resp

@app.route('/comments/article/<uuid:id>', methods = ['GET', 'DELETE'])
def comments(id):
    #get number of comments connected to an article
    if request.method == 'GET':
        mydb = db.get_db(SERVICE_NAME)

        try: 
            results = mydb.execute(mydb.prepare("SELECT COUNT(*) FROM comments WHERE article=?"), [id])
        except:
            e=sys.exc_info()[0]
            return conflict(e)
        if results[0][0]>0:
            resp = jsonify({
                "count": results[0][0]
            })
            resp.status_code = 200
            return resp
        else:
            return not_found()
            
    #remove a comment on an article
    elif request.method == 'DELETE':
        mydb = db.get_db(SERVICE_NAME)
        content = request.get_json()
        comment_id = content.get('CommentId', None)
        if comment_id == None:
            resp = jsonify({"error": "Error: Missing Arguments. Please specify CommentId to delete."})
            resp.status_code = 400
            return resp
        else:
            try:
                mydb.execute(mydb.prepare('DELETE FROM comments WHERE article=? AND id=? AND author=?'), [id, uuid.UUID(comment_id), auth.getUser()])
            except:
                e=sys.exc_info()[0]
                return conflict(e)
            try: 
                comments = mydb.execute(mydb.prepare("SELECT id, author, content, article, posted  FROM comments WHERE article=? ORDER BY id DESC"), [id])
            except:
                e=sys.exc_info()[0]
                return conflict(e)
            article_id = "/article/"+str(id)
            results = {'article_id': article_id,
                       'comments': []}
            for row in comments:
                results['comments'].append({
                    "id": row[0],
                    "author": row[1],
                    "content": row[2],
                    "article": row[3],
                    "posted": row[4],
                })
            resp = jsonify(results)
            resp.status_code = 200
            return resp
    else:
        resp = jsonify({'message': request.url + " contains no such method.",
                  'status': 405})
        return resp


        
#post comment to an article
@app.route('/comments/new/article/<uuid:id>', methods = ['POST'])
def post_comment(id):
    mydb = db.get_db(SERVICE_NAME)
    content = request.get_json()
    user=auth.getUser()

    body= content.get('text', None)
    if body==None:
        resp = jsonify({"message": "Error: Missing Arguments. Please specify Username and Comment Text"})
        resp.status_code = 400
        return resp 
    else:
        try:
            mydb.execute(mydb.prepare('INSERT INTO comments(id, posted, author, content, article) VALUES (now(), toTimestamp(now()), ?,?,?)'), [user, body, id])
        except:
            e=sys.exc_info()[0]
            return conflict(e)
        try:
            comments = mydb.execute(mydb.prepare("SELECT id,author,content,posted FROM comments WHERE article=? ORDER BY id DESC"), [id])
        except:
            e=sys.exc_info()[0]
            return conflict(e)
        article_id = "/article/"+ str(id)
        location = article_id + "/comments/"
        results = {'article_id': article_id,
                    'comments': []}
        for c in comments:
            results['comments'].append({
                "id": c[0],
                "author": c[1],
                "content": c[2],
                "posted": c[3],
            })
        resp = jsonify(results)
        resp.status_code = 200
        resp.headers['Location']=location
        return resp

        

#get n most recent article comments.
@app.route('/comments/<int:number>/article/<uuid:id>', methods=['GET'])
def getComments(id, number):
    mydb = db.get_db(SERVICE_NAME)
    try:
        results = mydb.execute("SELECT id, author, content, article, posted FROM comments WHERE article=%s ORDER BY id DESC LIMIT %s", (id, int(number)))
    except:
        e=sys.exc_info()[0]
        return conflict(e)

    results = list(results)
    if len(results) > 0:
        out = {
            "count": len(results),
            "comments": []
        }
        for row in results:
            out['comments'].append({
                "id": row[0],
                "author": row[1],
                "content": row[2],
                "article": row[3],
                "posted": row[4],
            })
        resp = jsonify(out)
        resp.status_code = 200
        return resp
    else:
        return not_found()

