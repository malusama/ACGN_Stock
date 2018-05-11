# -*- coding: utf-8 -*
from app.models import (
    # DBSession,
    base,
    User,
    Stock,
    Bank,
    Stock_Tag
)
import datetime
from .base import (
    check_args
)
from app.config import (
    redis_client,
    REQUEST_CACHE_TIMEOUT
)


def get_stock(user_id=None, limit=None, offset=None, order=None,
              company=None, factory=None, name=None, category=None,
              date_start=None, date_end=None):
    if limit is None:
        limit = 50
    if offset is None:
        offset = 0
    # content = redis_client.get(
    #     "id{}limit{}offset{}order{}".format(
    #         user_id, limit, offset, order))
    # if content:
    #     return [json.loads(content)[0], json.loads(content)[1]]
    session = base.DBSession()
    query_stock = session.query(Stock)
    if category and query_stock.filter(Stock.category.isnot(None)):
        query_stock = query_stock.filter(Stock.category.op(
            "~*")('(^|,).?({}).*?(,|$)'.format(category)))
    if company:
        query_stock = query_stock.filter(Stock.company == company)
    if factory:
        query_stock = query_stock.filter(Stock.factory == factory)
    if name:
        query_stock = query_stock.filter(Stock.name.like("%{}%".format(name)))
    if user_id:
        return query_stock.filter(Stock.id == user_id)
    if date_start:
        date_start = datetime.date(year=int(date_start.split('-')[0]),
                                   month=int(date_start.split('-')[1]),
                                   day=1)
        print(date_start)
        pass
    if date_end:
        pass
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


def get_user_stock(username=None):
    session = base.DBSession()
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


def get_stock_cover(stock_id):
    session = base.DBSession()
    cover = session.query(Stock).filter(
        Stock.id == stock_id).one_or_none()
    if cover:
        return cover.cover


@check_args
def get_stock_info(stock_id):
    # print(stock_id)
    session = base.DBSession()
    stock = session.query(Stock).filter(Stock.id == stock_id).one_or_none()
    tag = []
    if stock:
        stock_json = stock.to_json()
        if stock.category is not '':
            for i in stock.category.split(","):
                tag.append(session.query(Stock_Tag).filter(
                    Stock_Tag.id == i).one_or_none().tag)

            stock_json['category_name'] = ",".join(i for i in tag)
            print("类型:{}".format(stock_json['category']))
            pass
        else:
            stock_json['category_name'] = ''
        session.close()
        return stock_json
    else:
        return
