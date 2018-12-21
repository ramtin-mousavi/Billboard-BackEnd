import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager


app = Flask(__name__)
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace ("\\" , '/').split(':')[1]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+dir_path+'/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


DataBase = SQLAlchemy(app)
MarshMallow = Marshmallow (app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
login_manager.login_view = 'authentication.login'

@login_manager.user_loader
def load_user(user_id):
    return User_Model.query.get(user_id)



from Billboard.Authentication.models import User_Model
from Billboard.Authentication.controllers import authentication
from Billboard.Apps.controllers import apps
from Billboard.Gifts.controllers import gifts
from Billboard.Survey.controllers import surveys
from Billboard.Admin.controllers import admin
from Billboard.Profile.controllers import profile


app.register_blueprint(authentication)
app.register_blueprint(apps)
app.register_blueprint(gifts)
app.register_blueprint(surveys)
app.register_blueprint(admin)
app.register_blueprint(profile)
