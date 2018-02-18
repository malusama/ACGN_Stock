from app import (
    models,
)
import datetime


Tax = 1.1


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


def buy_stock(stock_id=None, order_number=None,
              order_price=None, user_name=None, order_type=None):
    # order_type 1是购买2是出售
    session = models.DBSession()
    if stock_id and order_type and order_number and order_price and user_name:
        order_type = int(order_type)
        order_number = int(order_number)
        order_price = int(order_price)
        if order_type == 1:
            stock_order = session.query(models.Stock_order).filter(
                models.Stock_order.stock_id == stock_id,
                models.Stock_order.stock_type == 2
            ).order_by(models.Stock_order.stock_price).first()
            user = session.query(models.User).filter(
                models.User.nickname == user_name).first()
            if user.currency < order_number * order_price * Tax:
                return -2
                # 返回-2 是用户所拥有的代币不足够完成操作
            if stock_order.stock_price <= order_price:
                if stock_order.stock_number <= order_number:
                    while order_number > 0:
                        if stock_order and \
                                stock_order.stock_price <= order_price and \
                                stock_order.stock_number <= order_number:
                            user.currency = user.currency - \
                                (stock_order.stock_number *
                                    order_price * Tax)
                            sell_user = session.query(models.User).filter(
                                models.User.id == stock_order.user_id).first()
                            sell_user.currency = sell_user.currency + \
                                stock_order.stock_number * order_price
                            order_number = order_number - \
                                stock_order.stock_number
                            session.delete(stock_order)
                            session.commit()
                            stock_order = session.query(
                                models.Stock_order).filter(
                                models.Stock_order.stock_id == stock_id,
                                models.Stock_order.stock_type == 2
                            ).order_by(models.Stock_order.stock_price).first()
                        elif stock_order and \
                                stock_order.stock_price <= order_price:
                            user.currency = user.currency - \
                                (order_number *
                                    order_price * Tax)

                            sell_user = session.query(models.User).filter(
                                models.User.id == stock_order.user_id).first()
                            sell_user.currency = sell_user.currency + \
                                order_number * order_price

                            stock_order.stock_number = \
                                stock_order.stock_number - order_number
                            session.commit()
                            order_number = 0
                        else:
                            sub = models.Stock_order(
                                user_id=user.id,
                                stock_id=stock_id,
                                stock_number=order_number,
                                stock_price=order_price,
                                stock_type=1)
                            session.add(sub)
                            session.commit()
                            order_number = 0
                else:
                    user.currency = user.currency - \
                        (order_number * order_price * Tax)
                    stock_order.stock_number = \
                        stock_order.stock_number - order_number
                    session.commit()
            else:
                sub = models.Stock_order(
                    user_id=user.id,
                    stock_id=stock_id,
                    stock_number=order_number,
                    stock_price=order_price,
                    stock_type=1)
                user.currency = user.currency - \
                    (order_number * order_price * Tax)
                session.add(sub)
                session.commit()
                return -1
                # 返回结果是-1 则是卖方市场没有匹配到合适的价格 挂到市场
            return 1
        elif order_type == 2:

            stock_order = session.query(models.Stock_order).filter(
                models.Stock_order.stock_id == stock_id,
                models.Stock_order.stock_type == 1
            ).order_by(-models.Stock_order.stock_price).first()

            user = session.query(models.User).filter(
                models.User.nickname == user_name).first()

            sell_stock = session.query(models.Bank).filter(
                models.Bank.user_id == user.id,
                models.Bank.stock_id == stock_id).first()
            if sell_stock and sell_stock.stock_number >= order_number:

                if stock_order.stock_price >= order_price:
                    if stock_order.stock_number < order_number:
                        while order_number > 0:
                            if stock_order and \
                                    stock_order.stock_price >= \
                                    order_price and \
                                    stock_order.stock_number <= order_number:
                                print(stock_order.stock_price)
                                user.currency = user.currency + \
                                    (order_number * order_price * Tax)

                                sell_user = session.query(models.User).filter(
                                    models.User.id == user.id).first()
                                sell_user.currency = sell_user.currency + \
                                    stock_order.stock_number * order_price

                                buy_user = session.query(models.User).filter(
                                    models.User.id ==
                                    stock_order.user_id).first()
                                buy_user.currency = buy_user.currency + \
                                    (stock_order.stock_price - order_price) * \
                                    stock_order.stock_number

                                order_number = order_number - \
                                    stock_order.stock_number

                                session.delete(stock_order)
                                session.commit()
                                stock_order = session.query(
                                    models.Stock_order).filter(
                                    models.Stock_order.stock_id == stock_id,
                                    models.Stock_order.stock_type == 1
                                ).order_by(
                                    -models.Stock_order.stock_price).first()
                            elif stock_order and \
                                    stock_order.stock_price >= order_price:
                                user.currency = user.currency + \
                                    (order_number *
                                     order_price * Tax)

                                sell_user = session.query(models.User).filter(
                                    models.User.id ==
                                    stock_order.user_id).first()
                                sell_user.currency = sell_user.currency + \
                                    ((stock_order.stock_price -
                                      order_price) * stock_order.stock_number)

                                stock_order.stock_number = \
                                    stock_order.stock_number - order_number
                                session.commit()
                                order_number = 0
                            else:
                                print(order_number)
                                sub = models.Stock_order(
                                    user_id=user.id,
                                    stock_id=stock_id,
                                    stock_number=order_number,
                                    stock_price=order_price,
                                    stock_type=2)
                                session.add(sub)
                                session.commit()
                                order_number = 0
                else:
                    user.currency = user.currency + \
                        (order_number * order_price * Tax)
                    stock_order.stock_number = \
                        stock_order.stock_number - order_number
                    session.commit()
            return 2
        else:
            return -3
            # 返回-3 是请求的参数错误
        return 1


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


def get_user_stock(username=None):
    session = models.DBSession()
    if username:
        user = session.query(models.User).filter(
            models.User.nickname == username).first()
        user_stock_index = session.query(models.Bank).filter(
            models.Bank.user_id == user.id).all()
        if user_stock_index:
            user_stock = []
            for iter in user_stock_index:
                temp = {}
                temp['stock_number'] = iter.stock_number
                temp['stock_id'] = iter.stock_id
                temp['name'] = iter.stock.name
                user_stock.append(temp)
            return user, user_stock

    else:
        return None


def get_stock_order(stock_id=None, user_id=None, order_type=None):
    stock_order = []

    session = models.DBSession()
    if stock_id:
        if user_id:
            stock_order_index = session.query(
                models.Stock_order).filter(
                models.Stock_order.stock_id == stock_id,
                models.Stock_order.user_id == user_id,
                models.Stock_order.stock_type == order_type).all()

            for iter in stock_order_index:
                temp = {}
                temp['user_id'] = iter.user_id
                temp['stock_number'] = iter.stock_number
                stock_order.append(temp)
            return stock_order
        else:
            stock_order_index = session.query(
                models.Stock_order).filter(
                models.Stock_order.stock_id == stock_id,
                models.Stock_order.stock_type == order_type).all()
            for iter in stock_order_index:
                temp = {}
                temp['user_id'] = iter.user_id
                temp['stock_number'] = iter.stock_number
                temp['stock_price'] = iter.stock_price
                stock_order.append(temp)
            return stock_order
