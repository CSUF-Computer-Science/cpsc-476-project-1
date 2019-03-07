import sys, sqlite3, bcrypt, base64, hashlib, bcrypt
from flask import Flask, request, g, jsonify, Response
from .data import db as database, auth

app = Flask(__name__)
database.init_app(app)
basic_auth = auth.GetAuth()
basic_auth.init_app(app)

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
          hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.get_json()['password'].encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe')
          full_name = request.get_json()['full_name']
          db = database.get_db()       
          for row in db.execute('SELECT username FROM users WHERE username=(?);', [username,]):
               if row != None:
                    database.close_db()
                    message = jsonify({'error':'HTTP 409 Conflict'})
                    message.status_code = 409
                    return message
          db.execute('INSERT INTO users(username, password, full_name) VALUES (?,?,?);', [username, hashed, full_name])
          db.commit()
          database.close_db()
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
          hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe')
          print(username, hashed)
          db = database.get_db()
          for row in db.execute('SELECT username FROM users WHERE username=(?);', [username,]):
               if row != None:
                    db.execute('DELETE FROM users WHERE username=(?) AND password=(?);', [username, hashed])
                    db.commit()
                    database.close_db()
                    print('deleted')
                    message = jsonify({'success':'user exists'})
                    message.status_code = 200
                    return message
               else:
                    message = jsonify({'error':'user doesnt exist'})
                    message.status_code = 401
                    database.close_db()
                    return message

@app.route('/user/changepw', methods=['POST'])
@basic_auth.required
def change_password():
     if request.method == 'POST':
          user = request.headers['Authorization'].strip().split(' ')
          username, password = base64.b64decode(user[1]).decode().split(':', 1)
          hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe')
          newhashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.get_json()['password'].encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe')
          db = database.get_db()
          for row in db.execute("SELECT username FROM users WHERE username=(?) AND password=(?);", [username, hashed]):
               if row != None:
                    db.execute("UPDATE users SET password=(?) WHERE username=(?) AND password=(?);", [newhashed, username, hashed])
                    db.commit()
                    database.close_db()
                    message = jsonify({"success":"password updated"})
                    message.status_code=200
                    return message
               db.close_db()
               message = jsonify({"error":"could not change password"})
               message.status_code=404
               return message

if __name__ == '__main__':
     basic_auth.init_app(app)
     app.run(host='127.0.0.1:5000')
