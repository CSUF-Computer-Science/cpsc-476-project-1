from flask_basicauth import BasicAuth
from flask.cli import with_appcontext
from . import db as database

class GetAuth(BasicAuth):
    print("entered auth")
    def check_credentials(self, username, password):
        print("in auth")
        db = database.get_db()
        if db.execute("SELECT username FROM users WHERE username=(?) AND password=(?);", [username,password]) != None:
            db.commit()
            database.close_db()
            return True
        else:
            print("bad auth")
            return False