import sys
from flask import Flask, request, g, jsonify, Response
import sqlite3
from .data import db as database
app = Flask(__name__)

database.init_app(app)

@app.route('/article/new', methods=['POST'])
def new_article():
    if request.method == 'POST':

    return

@app.route('/article/find', methods=['GET'])
def find_article():
    
    return
@app.route
if __name__ == '__main__':
     app.run(host="127.0.0.1:5001")