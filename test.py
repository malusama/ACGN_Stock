from app import models, handle
import datetime
session = models.DBSession()
user = session.query(models.Stock).all()
# u = models.User(nickname='malu', email='malu@email.com')
# print(user.password)
# print(handle.authorization('malu','chensicheng'))
# p = models.Post(body='my first post!',
#                created_at=datetime.datetime.utcnow(), author=user)
# session.add(p)
# session.commit()
for iter in user:
	print(iter.name)