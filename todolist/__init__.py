from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import timedelta


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")
# print("->", SECRET_KEY, DB_NAME)

def create_database(app):
    if not os.path.exists('todolist/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created BD!")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    
    db.init_app(app)
    create_database(app)
    from todolist.user import user
    from todolist.views import views
    from .models import Note, User

    app.register_blueprint(user)
    app.register_blueprint(views)

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes = 1)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


