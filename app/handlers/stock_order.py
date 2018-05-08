# -*- coding: utf-8 -*
from app.models import (
    # DBSession,
    base,
    Stock_order,
)
from .base import (
    check_args
)
from app.config import (
    redis_client,
    REQUEST_CACHE_TIMEOUT
)


@check_args
def get_stock_order(stock_id=None, user_id=None, order_type=None):
    stock_order = []

    session = base.DBSession()
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
