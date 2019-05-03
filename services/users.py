import base64, hashlib, bcrypt, os, sys
from flask import Flask, request, jsonify
from .data import db as database, auth
import re

SERVICE_NAME = os.path.splitext(os.path.basename(__file__))[0]

app = Flask(__name__)
database.init_app(app)

basic_auth = auth.GetAuth()
basic_auth.init_app(app)

allow_anon_auth = auth.AllowAnonymousAuth()
allow_anon_auth.init_app(app)

def authReq(originalURI):
     paths={
          '/article/new':basic_auth,
          '/article/delete/\d+':basic_auth,
          '/article/edit/\d+':basic_auth,
          '/comments/article/\d+':basic_auth,
          '/tags/article/\d+':basic_auth,
          '/user/delete':basic_auth,
          '/user/changepw':basic_auth,
          '\/comments\/new\/article\/\d+':allow_anon_auth
     }

     for path,auth in paths.items():
         if re.search(path,originalURI):
              return auth
     
     return None

@app.route('/auth')
def authorize():
     authType = authReq(request.headers['X-Original-URI'])

     if authType and not authType.authenticate():
          resp=jsonify({'status': 'Unauthorized user'})
          resp.status_code = 401
     else:
          resp=jsonify({'status': 'OK'})
          resp.status_code = 200
     return resp


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
        'message': 'Error: Conflict at ' + request.url +' Code '+ error.message
    }
    resp = jsonify(message)
    resp.status_code = 409
    return resp

@app.route('/user/register', methods=['POST'])
def register_user():
     if request.method == 'POST':
          username = request.get_json()['username']
          hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.get_json()['password'].encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
          full_name = request.get_json()['full_name']
          db = database.get_db(SERVICE_NAME)
          for row in db.execute(db.prepare('SELECT username FROM users WHERE username=?;'), [username]):
               if row != None:
                    message = jsonify({'error':'HTTP 409 Conflict'})
                    message.status_code = 409
                    return message
          db.execute(db.prepare('INSERT INTO users(username, password, full_name) VALUES (?,?,?);'), [username, hashed, full_name])
          message = jsonify({'success':'username has been registered'})
          message.status_code = 200
          return message

@app.route('/user/delete', methods=['POST'])
@basic_auth.required
def delete_user():
     if request.method == 'POST':
          #decoding user authorization
          user = request.headers['Authorization'].strip().split(' ')
          username, password = base64.b64decode(user[1]).decode().split(':', 1)
          db = database.get_db(SERVICE_NAME)
          for row in db.execute(db.prepare('SELECT username FROM users WHERE username=?;'), [username]):
               if row != None:
                    db.execute(db.prepare('DELETE FROM users WHERE username=?;'), [username])
                    message = jsonify({'success':'user deleted'})
                    message.status_code = 200
                    return message
               else:
                    message = jsonify({'error':'user doesnt exist'})
                    message.status_code = 401
                    return message

@app.route('/user/changepw', methods=['POST'])
@basic_auth.required
def change_password():
     if request.method == 'POST':
          user = request.headers['Authorization'].strip().split(' ')
          username, password = base64.b64decode(user[1]).decode().split(':', 1)
          hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
          newhashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.get_json()['password'].encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
          db = database.get_db(SERVICE_NAME)
          for row in db.execute(db.prepare("SELECT username FROM users WHERE username=?;"), [username]):
               if row != None:
                    db.execute(db.prepare("UPDATE users SET password=? WHERE username=?;"), [newhashed, username])
                    message = jsonify({"success":"password updated"})
                    message.status_code=200
                    return message
               message = jsonify({"error":"could not change password"})
               message.status_code=404
               return message
