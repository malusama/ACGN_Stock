# -*- coding: utf-8 -*
from app.models import (
    # DBSession,
    base,
    User,
    Bank,
    Stock_order,
)
from .base import (
    check_args
)
from app.config import (
    redis_client,
    REQUEST_CACHE_TIMEOUT
)
Tax = 1.1


def buy_stock(stock_id=None, order_number=None,
              order_price=None, user_name=None, order_type=None):
    # order_type 1是购买2是出售
    order_number = int(order_number)
    order_price = int(order_price)
    order_type = int(order_type)
    stock_id = int(stock_id)
    session = base.DBSession()
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
