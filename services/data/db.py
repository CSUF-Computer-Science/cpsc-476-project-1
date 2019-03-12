import sqlite3, click, os.path
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
        db.execute("PRAGMA foreign_keys = on")
    return db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with current_app.app_context():
        db = get_db()
    with current_app.open_resource('data/schema.sql') as f:
        content = f.read().decode()
        db.executescript(content)
    db.commit()

def reset_db():
    if os.path.isfile("newkids.db"):
        os.remove("newkids.db")
    
def init_data():
    if not os.path.isfile("newkids.db"):
        init_db()
    db=get_db()
    db.execute('INSERT INTO users (username, password, full_name) VALUES ("testuser", "$2b$12$DbmIZ/a5LByoJHgFItyZCeyg/DVecJAzVzmtVfFGKioGo8AqWE1XC", "Test User")')
    db.execute('INSERT INTO articles (title, content, author) VALUES ("My Fake Twitter BIO", "I\'m a cat fan", "testuser")')
    db.execute('INSERT INTO comments (author, article, content) VALUES ("testuser", 1, "that\'s super cool")')
    db.execute('INSERT INTO tags (article, name) VALUES (1, "blessed")')
    db.execute('INSERT INTO tags (article, name) VALUES (1, "stayblessed")')
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_cmd():
    init_db()
    click.echo("Init the db")

@click.command('reset-db')
@with_appcontext
def reset_db_cmd():
    reset_db()
    init_db()
    click.echo("Reset the db")


@click.command('init-data')
@with_appcontext
def init_data_cmd():
    init_data()
    click.echo("Db initialized with data")