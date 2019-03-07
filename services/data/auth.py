import bcrypt, base64, hashlib
from flask_basicauth import BasicAuth
from flask.cli import with_appcontext
from . import db as database

class GetAuth(BasicAuth):
    def check_credentials(self, username, password):
        hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe')
        db = database.get_db()
        results = db.execute('SELECT username, password FROM users WHERE username=(?) AND password=(?);', [username, hashed.decode()]).fetchall()
        return len(results) == 1