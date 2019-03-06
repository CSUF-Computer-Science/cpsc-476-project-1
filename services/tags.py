import sqlite3
import click
from flask import g, Flask, Response, jsonify
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


@app.route('/tags/<tagname>', methods['GET','POST','DELETE'])
def tagSearch(tagname):
    mydb = db.get_db()

    if request.method=='GET':
        results = db.execute("SELECT * FROM tags WHERE name=?",[tagname]).fetchall()
        if results:
            resp= jsonify(results)
            resp.status_code=200
            db.close_db()
            return resp
        else:
            db.close_db()
            return not_found()
    elif request.method=='POST':
        content=request.get_json()
        id=content.get('ID'), None
        if id == None:
            resp=jsonify({ "error": "Error: Missing Arguments. Please specify article id." })
            resp.status_code=400
            return resp
        else:
            mydb.execute(
                'INSERT INTO tags(name, article)''VALUES (?,?)', [id, tagname])
            db.commit()
            



@app.route('/tags/remove', methods=['DELETE'])
def removeTag():
    if request.method == 'DELETE':
        if 'TagName', 'ID' in request.args:
        mydb = db.get_db()
        tagname = request.args['TagName']
        id = request.args['ID']
        print(tagname, id)
        mydb.execute(
            'DELETE FROM tags WHERE name=(tagname) AND article=(id)''VALUES (?,?)', [tagname, id])
        mydb.commit()
        mydb.close_db()
        return "Success!"
        else:
            return "Error: Missing Arguments. Please specify a TagName and URL. "
