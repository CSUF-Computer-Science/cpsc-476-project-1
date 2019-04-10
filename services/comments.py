import sys, os
from flask import Flask, jsonify, request
from .data import db, auth

SERVICE_NAME = os.path.basename(__file__)

app = Flask(__name__, instance_relative_config=True)
app.config["DEBUG"] = True
db.init_app(app)

basic_auth = auth.GetAuth()
basic_auth.init_app(app)

allow_anon_auth = auth.AllowAnonymousAuth()
allow_anon_auth.init_app(app)

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

@app.errorhandler(409)
def conflict(error=None):
    message = {
        'status': 409,
        'message': 'Error: Conflict at ' + request.url +' Code '+ str(error)
    }
    resp = jsonify(message)
    resp.status_code = 409
    return resp

@app.route('/article/<id>/comments', methods = ['GET', 'POST'])
@allow_anon_auth.required
def comments(id):
    #get number of comments connected to an article
    if request.method == 'GET':
        mydb = db.get_db(SERVICE_NAME)
        try: 
            results = mydb.execute(
                "SELECT COUNT(*) FROM comments WHERE article=?", [id]).fetchall()
        except:
            e=sys.exc_info()[0]
            return conflict(e)
        if results[0][0]>0:
            resp = jsonify({
                "count": results[0][0]
            })
            resp.status_code = 200
            db.close_db(SERVICE_NAME)
            return resp
        else:
            db.close_db(SERVICE_NAME)
            return not_found()
            
    #post a new comment on an article
    elif request.method == 'POST':
        mydb = db.get_db(SERVICE_NAME)
        content = request.get_json()
        user= auth.getUser()
        body= content.get('text', None)
        if body==None:
            resp = jsonify({"error": "Error: Missing Arguments. Please specify Username and Comment Text"})
            resp.status_code = 400
            return resp
        else:
            try:
                mydb.execute(
                    'INSERT INTO comments(author, content, article) VALUES (?,?,?)', [user, body, id])
            except:
                e=sys.exc_info()[0]
                return conflict(e)
            mydb.commit()
            try:
                comments = mydb.execute(
                    "SELECT id,author,content,posted FROM comments WHERE article=? ORDER BY posted DESC", [id]).fetchall()
            except:
                e=sys.exc_info()[0]
                return conflict(e)
            db.close_db(SERVICE_NAME)
            article_id = "/article/"+ id
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
    else:
        resp = jsonify({'message': request.url + " contains no such method.",
                  'status': 405})
        return resp

#delete comment from an article
@app.route('/article/<id>/delete_comments', methods = ['DELETE'])
@basic_auth.required
def delete_comment(id):
    if request.method == 'DELETE':
        mydb = db.get_db(SERVICE_NAME)
        content = request.get_json()
        comment_id = content.get('CommentId', None)
        if comment_id == None:
            resp = jsonify({"error": "Error: Missing Arguments. Please specify TagName(s) to add."})
            resp.status_code = 400
            return resp
        else:
            try:
                mydb.execute('DELETE FROM comments WHERE id=? AND article=?', [comment_id, id])
            except:
                e=sys.exc_info()[0]
                return conflict(e)
            mydb.commit()
            try: 
                comments = mydb.execute(
                    "SELECT * FROM comments WHERE article=? ORDER BY posted DESC", [id]).fetchall()
            except:
                e=sys.exc_info()[0]
                return conflict(e)
            db.close_db(SERVICE_NAME)
            article_id = "/article/"+id
            results = {'article_id': article_id,
                       'comments': []}
            for c in comments:
                results['comments'].append({

                })
            resp = jsonify(results)
            resp.status_code = 200
            return resp
    else:
        resp = jsonify({'message': request.url + " contains no such method.",
                  'status': 405})
        return resp

#get n most recent article comments.
@app.route('/article/<id>/comments/<number>', methods=['GET'])
def getComments(id, number):
    mydb = db.get_db(SERVICE_NAME)
    try:
        results = mydb.execute(
            "SELECT * FROM (SELECT id,author,content,article,posted FROM comments WHERE article=? ORDER BY posted DESC) LIMIT ?", [id, number]).fetchall()
    except:
        e=sys.exc_info()[0]
        return conflict(e)

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
        db.close_db(SERVICE_NAME)
        return resp
    else:
        db.close_db(SERVICE_NAME)
        return not_found()

