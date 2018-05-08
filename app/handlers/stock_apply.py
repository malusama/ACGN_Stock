# -*- coding: utf-8 -*
from app.models import (
    # DBSession,
    base,
    User,
    Bank,
    Stock,
    Stock_apply,
)
from .base import (
    check_args
)
from app.config import (
    redis_client,
    REQUEST_CACHE_TIMEOUT
)


def get_apply():
    session = base.DBSession()
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


@check_args
def stock_apply(user_id, stock_name, stock_image,
                stock_cover, stock_introduction, apply_status):
    session = base.DBSession()
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        return "用户不存在"
    submit = Stock_apply(user_id=user.id, stock_name=stock_name,
                         image=stock_image, cover=stock_cover,
                         introduction=stock_introduction, apply_status=0)
    session.add(submit)
    session.commit()
    return "提交成功"


def review_pass(stock_id):
    if stock_id:
        session = base.DBSession()
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
