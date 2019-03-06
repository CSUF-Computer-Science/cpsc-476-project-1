import sys
from flask import Flask, request, g, jsonify, Response
import sqlite3
from .data import db as database, auth
app = Flask(__name__)

database.init_app(app)
basic_auth = auth.GetAuth()
basic_auth.init_app(app)

@app.route('/article/new', methods=['POST'])#return 201 with URL in header
@basic_auth.required
def new_article():
    if request.method == 'POST':
        print(request)
        db = database.get_db()
        
    return

@app.route('/article/<int:article_id>', methods=['GET'])#return 200 else 404
def find_article():

    return

@app.route('/article/edit', methods=['POST'])#return 200 or 404
@basic_auth.required
def edit_article():

    return

if __name__ == '__main__':
     app.run(host="http://127.0.0.1:5001")