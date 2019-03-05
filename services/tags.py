import sqlite3
import click
from flask import g, Flask
from .data import db
app=Flask(__name__)
db.init_app(app)

""" @app.route('/')
def my function here """
