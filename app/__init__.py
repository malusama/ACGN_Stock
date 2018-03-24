import os
from flask import Flask
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = '123456'

from app.views import (
    views
)
from app.models import (
    models
)
