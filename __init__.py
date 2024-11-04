from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "userinfo.db"

def create_app():
    #Creating app, secret key, and database
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "HawkI"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from tables import User

    #Create SQL db
    with app.app_context():
        db.create_all()


    #Setting up login capabilities
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    #Get User ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

