import bcrypt, base64, hashlib
from flask_basicauth import BasicAuth
from flask.cli import with_appcontext
from flask import request
from . import db as database

class GetAuth(BasicAuth):
    def check_credentials(self, username, password):
        hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
        db = database.get_db()
        results = db.execute('SELECT password FROM users WHERE username=(?);', [username]).fetchall()
        if len(results) > 0:
            dbPass = results[0][0]

            if hashed == dbPass:
                request.user = {
                    "username": username
                }
                return True
            else:
                return False
        else:
            return False

# Always lets a user through to a view, but will set their username
# to "Anonymous Coward" in the request object if the user doesn't
# properly authenticate with the database.
class AllowAnonymousAuth(BasicAuth):
    def check_credentials(self, username, password):
        hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
        db = database.get_db()
        results = db.execute('SELECT password FROM users WHERE username=(?);', [username]).fetchall()
        if len(results) > 0:
            dbPass = results[0][0]

            request.user = {
                "username": hashed == dbPass and username or "Anonymous Coward"
            }
        else:
            request.user = {
                "username": "Anonymous Coward"
            }

        return True

def getUser():
    print(request.user)
    return (hasattr(request, "user") and request.user["username"]) or "Anonymous Coward"
