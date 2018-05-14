from flask import Flask
import os
import redis


redis_client = redis.Redis(host='localhost', port=6379,
                           db=0, decode_responses=True)
REQUEST_CACHE_TIMEOUT = 60 * 60 * 24   # 1 day


basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

app = Flask(__name__)
app.config.from_object('config')
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
