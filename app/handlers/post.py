# -*- coding: utf-8 -*
from app.models import (
    # DBSession,
    base,
    User,
    Post,

)
from app.config import (
    redis_client,
    REQUEST_CACHE_TIMEOUT
)


def get_post():
    # content = redis_client.get('post')
    # if content:
    #     return json.loads(content)
    session = base.DBSession()
    posts = session.query(Post).all()
    content = []
    for iter in posts:
        temp = {}
        temp['body'] = iter.body
        temp['user.id'] = iter.id
        user = session.query(User).filter(
            User.id == iter.user_id).first()
        if user:
            temp['username'] = user.nickname
        else:
            temp['username'] = 'None'
        content.append(temp)
    # redis_client.setex('post', json.dumps(content), REQUEST_CACHE_TIMEOUT)
    return content
