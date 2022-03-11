# __init__.py
 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


current_dir = os.getcwd()
#print(current_dir)
with open(current_dir + "/config.json", "r") as fp:
    config = fp.read()
config = json.loads(config)

def create_app():
    app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

    app.config['SECRET_KEY'] = 'ddLWGND4om3j4K3i4op1'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unblind.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_uid):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(user_uid)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

