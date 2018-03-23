import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir




app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = '123456'
lm = LoginManager(app)
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
from app.views import (
    views
)
from app.models import (
	models
)