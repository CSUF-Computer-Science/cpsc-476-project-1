from flask_basicauth import BasicAuth
from . import db as database
from flask.cli import with_appcontext

class GetAuth(BasicAuth):
    print("entered auth")
    @app_withcontext
    def check_credentials(self, username, password):
        db = database.get_db()
        if db.execute("SELECT username FROM users WHERE username=(?) AND password=(?);", [username,password]) != None:
            db.commit()
            database.close_db()
            return True
        else:
            return False