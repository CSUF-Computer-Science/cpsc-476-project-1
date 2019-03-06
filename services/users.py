import sys
from flask import Flask, request, g, jsonify, Response
import sqlite3
from .data import db as database, auth
app = Flask(__name__)

database.init_app(app)
basic_auth = auth.GetAuth()
basic_auth.init_app(app)

@app.route('/user/register', methods=['POST'])
def register_user():
     if request.method == 'POST':
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        full_name = request.get_json()["full_name"]
        db = database.get_db()
        if db.execute("SELECT username FROM users WHERE username=(?);", [username,]) != None:
             database.close_db()
             message = jsonify({"error":"HTTP 409 Conflict"})
             message.status_code = 409
             return message
        else:
             db.execute("INSERT INTO users(username, password, full_name) VALUES (?,?,?);", [username, password, full_name])
             db.commit()
             database.close_db()
             message = jsonify({"success":"username has been registered"})
             message.status_code = 200
        return message

@app.route('/user/delete', methods=['POST'])
@basic_auth.required
def delete_user():
     if request.method == 'POST':
          username = request.get_json()['username']
          password = request.get_json()['password']
          print(username, password)
          db = database.get_db()
          if db.execute("SELECT username FROM users WHERE username=(?) AND password=(?);", [username, password]) != None:
               db.execute("DELETE FROM users WHERE username=(?) AND password=(?);", [username, password])
               db.commit()
               database.close_db()
               print("deleted")
               message = jsonify({"success":"user exists"})
               message.status_code = 200
               return message
          else:
               message = jsonify({"error":"user doesnt exist"})
               message.status_code = 401
               database.close_db()
               return message

@app.route('/user/changepw', methods=['POST'])
# @basic_auth.required
def change_password():
     if request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        db = database.get_db()
        db.close_db()


if __name__ == '__main__':
     basic_auth.init_app(app)
     app.run(host="127.0.0.1:5000")
