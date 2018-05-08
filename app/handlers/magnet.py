# -*- coding: utf-8 -*
from app.models import (
    # DBSession,
    base,
    Stock_Magnet,
)
from .base import (
    check_args
)
from app.config import (
    redis_client,
    REQUEST_CACHE_TIMEOUT
)


def getMagenet(stock_id):
    if stock_id:
        session = base.DBSession()
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
    session = base.DBSession()
    sub = Stock_Magnet(stock_id=stock_id, magnet=Magnet, user_id=user_id)
    session.add(sub)
    session.commit()
    session.close()
    return "成功"
    pass
