from app import models, handle

Tax = 1.1


def tset_data(user_id=None, stock_id=None, stock_number=None,
              stock_type=None, stock_price=None):
    session = models.DBSession()
    u = models.Stock_order(user_id=user_id,
                           stock_id=stock_id,
                           stock_number=stock_number,
                           stock_type=stock_type,
                           stock_price=stock_price)
    session.add(u)
    session.commit()
    session.close()


def buy_stock(stock_id=None, order_number=None,
              order_price=None, user_name=None, order_type=None):
    # order_type 1是购买2是出售
    order_number = int(order_number)
    order_price = int(order_price)
    order_type = int(order_type)
    stock_id = int(stock_id)
    session = models.DBSession()
    if stock_id and order_type:
        if order_type == 1:
            stock_order = session.query(models.Stock_order).filter(
                models.Stock_order.stock_id == stock_id,
                models.Stock_order.stock_type == 2
            ).order_by(models.Stock_order.stock_price).first()
            user = session.query(models.User).filter(
                models.User.nickname == user_name).first()

            bank = session.query(models.Bank).filter(
                models.Bank.user_id == user.id,
                models.Bank.stock_id == stock_id).first()

            if user.currency < int(order_number) * int(order_price) * Tax:
                return "用户所拥有的代币不足够完成操作"
            if stock_order is None:
                # 如果卖方市场没有订单 则直接提交至挂单
                sub = models.Stock_order(
                    user_id=user.id,
                    stock_id=stock_id,
                    stock_number=order_number,
                    stock_price=order_price,
                    stock_type=1)
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
                            sell_user = session.query(models.User).filter(
                                models.User.id == stock_order.user_id).first()
                            sell_user.currency = sell_user.currency + \
                                stock_order.stock_number * order_price
                            order_number = order_number - \
                                stock_order.stock_number
                            session.delete(stock_order)
                            if bank:
                                sub = models.Bank(
                                    user_id=user.id,
                                    stock_id=stock_id,
                                    stock_number=stock_order.stock_number)
                                session.add(sub)
                            else:
                                bank.stock_number = bank.stock_number + \
                                    stock_order.stock_number
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
                            if bank:
                                sub = models.Bank(
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
                            sub = models.Stock_order(
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
                return "卖方市场没有匹配到合适的价格 挂到市场"
        elif order_type == 2:
            stock_order = session.query(models.Stock_order).filter(
                models.Stock_order.stock_id == stock_id,
                models.Stock_order.stock_type == 1
            ).order_by(-models.Stock_order.stock_price).first()
            # 买方市场订单
            user = session.query(models.User).filter(
                models.User.nickname == user_name).first()
            bank = session.query(models.Bank).filter(
                models.Bank.user_id == user.id,
                models.Bank.stock_id == stock_id).first()
            if bank is None or bank.stock_number < int(order_number):
                return "用户所拥有的股票数不够"
            else:
                bank.stock_number = bank.stock_number - order_number
                session.commit()
            if stock_order is None:
                # 如果买方市场没有订单 则直接提交至挂单
                sub = models.Stock_order(
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
                            print(stock_order.stock_price)
                            user.currency = user.currency + \
                                (order_number * order_price * Tax)

                            sell_user = session.query(models.User).filter(
                                models.User.id == user.id).first()
                            sell_user.currency = sell_user.currency + \
                                stock_order.stock_number * order_price

                            buy_user = session.query(models.User).filter(
                                models.User.id == stock_order.user_id).first()
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
                            ).order_by(-models.Stock_order.stock_price).first()
                        elif stock_order and \
                                stock_order.stock_price >= order_price:
                            user.currency = user.currency + \
                                (order_number *
                                    order_price * Tax)

                            sell_user = session.query(models.User).filter(
                                models.User.id == stock_order.user_id).first()
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
                sub = models.Stock_order(
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


def run():
    '''
    for iter in range(1, 5):
        tset_data(user_id=3, stock_id=2, stock_number=1,
                  stock_type=1, stock_price=iter)
        tset_data(user_id=3, stock_id=1, stock_number=1,
                  stock_type=1, stock_price=iter)
        tset_data(user_id=3, stock_id=2, stock_number=1,
                  stock_type=2, stock_price=10 - iter)
        tset_data(user_id=3, stock_id=1, stock_number=1,
                  stock_type=2, stock_price=10 - iter)
    '''
    # tset_data(user_id=3, stock_id=2, stock_number=5,
    #          stock_type=1, stock_price=5)
    print(buy_stock(stock_id=1, order_number=2,
                    order_price=2, user_name='admin', order_type=2))
    '''
    session = models.DBSession()
    order = session.query(models.Stock_order).filter(
        models.Stock_order.stock_type == 1).order_by(
        models.Stock_order.stock_price).all()
    for iter in order:
        print(iter.stock_price)
    '''


if __name__ == '__main__':
    run()
    # print(handle.get_stock_cover(1))
