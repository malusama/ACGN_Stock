# -*- coding: utf-8 -*
from app.models import (
    DBSession,
    User,
    Stock,
    Bank,
    Stock_order,
    Post,
    Stock_apply,
    Stock_Magnet,
    Stock_Tag
)
from .base import (
    check_args
)
from app.config import (
    redis_client,
    REQUEST_CACHE_TIMEOUT
)
import json


Tax = 1.1


def authorization(user, password):
    session = DBSession()
    dbuser = session.query(User).filter(
        User.nickname == user).first()
    if dbuser is not None:
        if dbuser.password == password:
            session.close()
            return True
    session.close()
    return False


def register(user, password, email):
    if user is '':
        return False
    if password is '':
        return False
    if email is '':
        return False
    session = DBSession()
    userinfo = User(nickname=user,
                    password=password,
                    email=email)
    session.add(userinfo)
    session.commit()
    session.close()
    return True


def get_stock(user_id=None, limit=None, offset=None, order=None,
              company=None, factory=None, name=None, category=None):
    if limit is None:
        limit = 50
    if offset is None:
        offset = 0
    # content = redis_client.get(
    #     "id{}limit{}offset{}order{}".format(
    #         user_id, limit, offset, order))
    # if content:
    #     return [json.loads(content)[0], json.loads(content)[1]]
    session = DBSession()
    query_stock = session.query(Stock)
    if category:
        query_stock = query_stock.filter(Stock.category.in_(category))
    if company:
        query_stock = query_stock.filter(Stock.company == company)
    if factory:
        query_stock = query_stock.filter(Stock.factory == factory)
    if name:
        query_stock = query_stock.filter(Stock.name.like(name))
    if user_id:
        return query_stock.filter(Stock.id == user_id)
    count = query_stock.count()
    res = []
    stock = query_stock.offset(offset).limit(limit)
    for x in stock:
        res.append(x.to_json())
    # redis_client.setex("id{}limit{}offset{}order{}".format(
    #     id, limit, offset, order),
    #     json.dumps([count, res]),
    #     REQUEST_CACHE_TIMEOUT)
    return [count, res]


def buy_stock(stock_id=None, order_number=None,
              order_price=None, user_name=None, order_type=None):
    # order_type 1是购买2是出售
    order_number = int(order_number)
    order_price = int(order_price)
    order_type = int(order_type)
    stock_id = int(stock_id)
    session = DBSession()
    if stock_id and order_type:
        if order_type == 1:
            stock_order = session.query(Stock_order).filter(
                Stock_order.stock_id == stock_id,
                Stock_order.order_type == 2
            ).order_by(Stock_order.stock_price).first()
            user = session.query(User).filter(
                User.nickname == user_name).first()

            bank = session.query(Bank).filter(
                Bank.user_id == user.id,
                Bank.stock_id == stock_id).first()

            if user.currency < int(order_number) * int(order_price) * Tax:
                return "用户所拥有的代币不足够完成操作"
            if stock_order is None:
                # 如果卖方市场没有订单 则直接提交至挂单
                sub = Stock_order(
                    user_id=user.id,
                    stock_id=stock_id,
                    stock_number=order_number,
                    stock_price=order_price,
                    order_type=1)
                session.add(sub)
                session.commit()
                return "提交订单成功"
            if stock_order.stock_price <= order_price:
                if stock_order.stock_number <= order_number:
                    while order_number > 0:
                        if stock_order and \
                                stock_order.stock_price <= order_price and \
                                stock_order.stock_number <= order_number:
                            user.currency = user.currency - \
                                (stock_order.stock_number *
                                    order_price * Tax)
                            sell_user = session.query(User).filter(
                                User.id == stock_order.user_id).first()
                            sell_user.currency = sell_user.currency + \
                                stock_order.stock_number * order_price
                            order_number = order_number - \
                                stock_order.stock_number
                            session.delete(stock_order)
                            if bank:
                                sub = Bank(
                                    user_id=user.id,
                                    stock_id=stock_id,
                                    stock_number=stock_order.stock_number)
                                session.add(sub)
                            else:
                                bank.stock_number = bank.stock_number + \
                                    stock_order.stock_number
                            session.commit()
                            stock_order = session.query(
                                Stock_order).filter(
                                Stock_order.stock_id == stock_id,
                                Stock_order.order_type == 2
                            ).order_by(Stock_order.stock_price).first()
                        elif stock_order and \
                                stock_order.stock_price <= order_price:
                            user.currency = user.currency - \
                                (order_number *
                                    order_price * Tax)

                            sell_user = session.query(User).filter(
                                User.id == stock_order.user_id).first()
                            sell_user.currency = sell_user.currency + \
                                order_number * order_price

                            stock_order.stock_number = \
                                stock_order.stock_number - order_number
                            if bank:
                                sub = Bank(
                                    user_id=user.id,
                                    stock_id=stock_id,
                                    stock_number=order_number)
                                session.add(sub)
                            else:
                                bank.stock_number = bank.stock_number + \
                                    order_number
                            session.commit()
                            order_number = 0
                        else:
                            sub = Stock_order(
                                user_id=user.id,
                                stock_id=stock_id,
                                stock_number=order_number,
                                stock_price=order_price,
                                stock_type=1)
                            session.add(sub)
                            session.commit()
                            order_number = 0
                    return "购买成功"
                else:
                    user.currency = user.currency - \
                        (order_number * order_price * Tax)
                    stock_order.stock_number = \
                        stock_order.stock_number - order_number
                    session.commit()
                    return "购买成功"
            else:
                sub = Stock_order(
                    user_id=user.id,
                    stock_id=stock_id,
                    stock_number=order_number,
                    stock_price=order_price,
                    stock_type=1)
                user.currency = user.currency - \
                    (order_number * order_price * Tax)
                session.add(sub)
                session.commit()
                return "卖方市场没有匹配到合适的价格 挂到市场"
        elif order_type == 2:
            stock_order = session.query(Stock_order).filter(
                Stock_order.stock_id == stock_id,
                Stock_order.order_type == 1
            ).order_by(-Stock_order.stock_price).first()
            # 买方市场订单
            user = session.query(User).filter(
                User.nickname == user_name).first()
            bank = session.query(Bank).filter(
                Bank.user_id == user.id,
                Bank.stock_id == stock_id).first()
            if bank is None or bank.stock_number < int(order_number):
                return "用户所拥有的股票数不够"
            else:
                bank.stock_number = bank.stock_number - order_number
                session.commit()
            if stock_order is None:
                # 如果买方市场没有订单 则直接提交至挂单
                sub = Stock_order(
                    user_id=user.id,
                    stock_id=stock_id,
                    stock_number=order_number,
                    stock_price=order_price,
                    stock_type=2)
                session.add(sub)
                session.commit()
                return "出售成功"

            if stock_order.stock_price >= int(order_price):
                # 如果买方市场的价格高于当前出售价格
                if stock_order.stock_number < int(order_number):
                    # 如果买方市场的订单数量不够
                    while order_number > 0:
                        if stock_order and \
                                stock_order.stock_price >= order_price and \
                                stock_order.stock_number <= order_number:
                            # print(stock_order.stock_price)
                            user.currency = user.currency + \
                                (order_number * order_price * Tax)

                            sell_user = session.query(User).filter(
                                User.id == user.id).first()
                            sell_user.currency = sell_user.currency + \
                                stock_order.stock_number * order_price

                            buy_user = session.query(User).filter(
                                User.id == stock_order.user_id).first()
                            buy_user.currency = buy_user.currency + \
                                (stock_order.stock_price - order_price) * \
                                stock_order.stock_number

                            order_number = order_number - \
                                stock_order.stock_number

                            session.delete(stock_order)
                            session.commit()
                            stock_order = session.query(
                                Stock_order).filter(
                                Stock_order.stock_id == stock_id,
                                Stock_order.order_type == 1
                            ).order_by(-Stock_order.stock_price).first()
                        elif stock_order and \
                                stock_order.stock_price >= order_price:
                            user.currency = user.currency + \
                                (order_number *
                                    order_price * Tax)

                            sell_user = session.query(User).filter(
                                User.id == stock_order.user_id).first()
                            sell_user.currency = sell_user.currency + \
                                ((stock_order.stock_price -
                                    order_price) * stock_order.stock_number)

                            stock_order.stock_number = \
                                stock_order.stock_number - order_number
                            session.commit()
                            order_number = 0
                        else:
                            # print(order_number)
                            sub = Stock_order(
                                user_id=user.id,
                                stock_id=stock_id,
                                stock_number=order_number,
                                stock_price=order_price,
                                stock_type=2)
                            session.add(sub)
                            session.commit()
                            order_number = 0
                    return "出售成功"
                else:
                    user.currency = user.currency + \
                        (order_number * order_price * Tax)
                    stock_order.stock_number = \
                        stock_order.stock_number - order_number
                    if stock_order.stock_number == 0:
                        session.delete(stock_order)
                    session.commit()
                    return "出售成功"
            else:
                sub = Stock_order(
                    user_id=user.id,
                    stock_id=stock_id,
                    stock_number=order_number,
                    stock_price=order_price,
                    stock_type=2)
                session.add(sub)
                session.commit()
                return "出售成功"
        else:
            return '请求的参数错误'


def get_post():
    # content = redis_client.get('post')
    # if content:
    #     return json.loads(content)
    session = DBSession()
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


def get_user_stock(username=None):
    session = DBSession()
    if username:
        user = session.query(User).filter(
            User.nickname == username).first()
        user_stock_index = session.query(Bank).filter(
            Bank.user_id == user.id).all()
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
            return user, []

    else:
        return None, None


@check_args
def get_stock_order(stock_id=None, user_id=None, order_type=None):
    stock_order = []

    session = DBSession()
    if stock_id:
        if user_id:
            stock_order_index = session.query(
                Stock_order).filter(
                Stock_order.stock_id == stock_id,
                Stock_order.user_id == user_id,
                Stock_order.order_type == order_type).all()
            if stock_order_index:
                for iter in stock_order_index:
                    temp = {}
                    temp['user_id'] = iter.user_id
                    temp['stock_number'] = iter.stock_number
                    stock_order.append(temp)
                return stock_order
        else:
            stock_order_index = session.query(
                Stock_order).filter(
                Stock_order.stock_id == stock_id,
                Stock_order.order_type == order_type).all()
            if stock_order_index:
                for iter in stock_order_index:
                    temp = {}
                    temp['user_id'] = iter.user_id
                    temp['stock_number'] = iter.stock_number
                    stock_order.append(temp)
                return stock_order
    else:
        return stock_order


def get_stock_cover(stock_id):
    session = DBSession()
    cover = session.query(Stock).filter(
        Stock.id == stock_id).first()
    return cover.cover


@check_args
def stock_apply(user_id, stock_name, stock_image,
                stock_cover, stock_introduction, apply_status):
    session = DBSession()
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        return "用户不存在"
    submit = Stock_apply(user_id=user.id, stock_name=stock_name,
                         image=stock_image, cover=stock_cover,
                         introduction=stock_introduction, apply_status=0)
    session.add(submit)
    session.commit()
    return "提交成功"


def get_userid(username):
    if not username:
        raise ValueError
    session = DBSession()
    user = session.query(User).filter(User.nickname == username).first()
    if not user:
        return "没有用户"
    else:
        return str(user.id)


def get_user_authority(username):
    if not username:
        raise ValueError
    session = DBSession()
    user = session.query(User).filter(User.nickname == username).first()
    if not user:
        return "-1"
    else:
        return str(user.authority)


def get_apply():
    session = DBSession()
    stock_apply = session.query(Stock_apply).all()
    res = []
    if stock_apply:
        for iter in stock_apply:
            temp = {}
            temp['id'] = iter.id
            temp['user_id'] = iter.user_id
            temp['stock_name'] = iter.stock_name
            temp['stock_image'] = iter.image
            temp['stock_cover'] = iter.cover
            temp['stock_introduction'] = iter.introduction
            temp['apply_status'] = iter.apply_status
            res.append(temp)
    return res


def review_pass(stock_id):
    if stock_id:
        session = DBSession()
        review_stock = session.query(Stock_apply).filter(
            Stock_apply.id == stock_id).first()
        if review_pass:
            stock_name = review_stock.stock_name
            user_id = review_stock.user_id
            sub = Stock(name=review_stock.stock_name,
                        cover=review_stock.cover,
                        introduction=review_stock.introduction)
            session.add(sub)
            session.delete(review_stock)
            session.commit()
            # 用户增加股票
            stock = session.query(Stock).filter(
                Stock.name == stock_name).first()
            sub = Bank(user_id=user_id, stock_id=stock.id, stock_number=1000)
            session.add(sub)
            session.commit()
            return "成功"
        else:
            raise ValueError
    else:
        raise ValueError


def getMagenet(stock_id):
    if stock_id:
        session = DBSession()
        Magnet = session.query(
            Stock_Magnet).filter(Stock_Magnet.stock_id == stock_id).all()
        res = []
        for i in Magnet:
            # print(i)
            res.append(i.to_json())
        session.close()
        return res
    pass


@check_args
def addMagnet(stock_id, Magnet, user_id):
    session = DBSession()
    sub = Stock_Magnet(stock_id=stock_id, magnet=Magnet, user_id=user_id)
    session.add(sub)
    session.commit()
    session.close()
    return "成功"
    pass


@check_args
def get_stock_info(stock_id):
    # print(stock_id)
    session = DBSession()
    stock = session.query(Stock).filter(Stock.id == stock_id).first()
    tag = []
    for i in stock.category.split(","):
        tag.append(session.query(Stock_Tag).filter(
            Stock_Tag.id == i).first().tag)
    session.close()
    stock_json = stock.to_json()
    stock_json['category_name'] = ",".join(i for i in tag)
    # print("类型:{}".format(stock_json['category']))
    return stock_json
