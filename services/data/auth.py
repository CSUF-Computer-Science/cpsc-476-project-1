import bcrypt, base64, hashlib
from flask_basicauth import BasicAuth
from flask.cli import with_appcontext
from . import db as database

class GetAuth(BasicAuth):
    def check_credentials(self, username, password):
        hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe')
        db = database.get_db()
        for row in db.execute('SELECT username FROM users WHERE username=(?) AND password=(?);', [username, hashed]):
            if row != None:
                db.commit()
                database.close_db()
            return True
        else:
            print("bad auth")
            return False