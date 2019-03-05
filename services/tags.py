import sqlite3
import click
from flask import g, Flask
app=Flask(__name__)

@app.cli.command()
def init_db():
    with app.app_context():
        db=get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    click.echo("Init the db")

DATABASE='#'
""" @app.route('/')
def my function here """
def get_db():
    db=getattr(g,'_database', None)
    if db is None: 
        db=g.database=sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: 
        db.close()