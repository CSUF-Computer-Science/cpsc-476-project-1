import sqlite3
from flask import g

DATABASE = 'serrano.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()