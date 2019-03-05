import sys
from flask import Flask, request, g
import sqlite3
from .data import db as database
app = Flask(__name__)

database.init_app(app)


@app.route('/user/register', methods=['POST'])
def register_user():
     if request.method == 'POST':
        print(request)
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        print(username, password)
        db = database.get_db()
        db.execute("INSERT INTO users(username, password, full_name) VALUES (?,?,?)", [username, password, full_name])
        database.close_db()
        return username + ' added to database!'

@app.route('/user/delete', methods=['POST'])
def delete_user():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = database.get_db()
        db.execute("SELECT username FROM users WHERE (?,?)", username, password)
        database.close_db()


@app.route('/user/changepw', methods=['POST'])
def change_password():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = database.get_db()
        database.close_db()


if __name__ == '__main__':
    app.run()