import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

DATABASE = 'newkids.db'

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_cmd)

def get_db():
    db = getattr(g, '_database', None)
    if db not in g:
        db = g.database = sqlite3.connect(DATABASE)
    return db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with current_app.app_context():
        db = get_db()
    with current_app.open_resource('data/schema.sql') as f:
            db.executescript(f.read())
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_cmd():
    init_db()
    click.echo("Init the db")
