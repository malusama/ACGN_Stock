from app import (
    models,
)
import datetime


def authorization(user, password):
    session = models.DBSession()
    dbuser = session.query(models.User).filter(
        models.User.nickname == user).first()
    if dbuser is not None:
        if dbuser.password == password:
            return True
    return False


def register(user, password, email):
    if user is '':
        return False
    if password is '':
        return False
    if email is '':
        return False
    session = models.DBSession()
    userinfo = models.User(nickname=user,
                           password=password,
                           email=email)
    session.add(userinfo)
    session.commit()
    return True


def get_stock(id=None):
    session = models.DBSession()
    stock = []
    if id:
        stock_info = session.query(models.Stock).filter(
            models.Stock.id == id).all()
    else:
        stock_info = session.query(models.Stock).all()

    for iter in stock_info:
        temp = {}
        temp['id'] = iter.id
        temp['name'] = iter.name
        temp['total'] = iter.total
        temp['price'] = iter.price
        temp['introduction'] = iter.introduction
        temp['cover'] = iter.cover
        stock.append(temp)
    session.close()
    return stock


def buy_stock(id=None, number=None, user_name=None):
    session = models.DBSession()
    if id:
        stock = session.query(models.Stock).filter(
            models.Stock.id == id).first()
        user_money = session.query(models.User).filter(
            models.User.nickname == user_name).first()
        if number and stock.price and user_money:
            if (int(stock.price) * int(number)) > user_money.currency:
                return -1
                # 用户拥有的代币不够
            elif int(stock.total) < int(number):
                return -3
                # 股票数量不足
            else:
                money_change = models.Bank(
                    user_id=user_money.id, stock_id=id, stock_number=number)
                session.add(money_change)
                session.commit()
                user_money.currency = user_money.currency - \
                    (int(stock.price) * int(number))
                stock.total = stock.total - int(number)
                session.commit()
                session.close()
                return 1
        else:
            return -2
            # 输入数据错误


def get_post():
    session = models.DBSession()
    posts = session.query(models.Post).all()
    post = []
    for iter in posts:
        temp = {}
        temp['body'] = iter.body
        temp['user.id'] = iter.id
        user = session.query(models.User).filter(
            models.User.id == iter.user_id).first()
        if user:
            temp['username'] = user.nickname
        else:
            temp['username'] = 'None'
        post.append(temp)
    return post
