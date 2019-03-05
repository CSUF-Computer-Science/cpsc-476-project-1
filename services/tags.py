import sqlite3
import click
from flask import g, Flask
from .data import db
app=Flask(__name__, instance_relative_config=True)
db.init_app(app)
mydb=db.get_db()

#@app.route('/tags')
#def my function here """

def addToExisting():
    if request.method=='POST':
        #uncertain how to handle incoming here
        tagname=request.TagName
        URL=request.UrL

    mydb.execute(){
        'INSERT INTO tags(name, article)'
        'VALUES (?,?,?)',
        (URL, tagname)
    }
    mydb.commit()

def addToNew():
    if request.method=='POST':
        #uncertain how to handle incoming here
        tagname=request.TagName
        URL=
