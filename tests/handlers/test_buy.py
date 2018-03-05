from app.handlers import (
    handle
)
from app.models import (
    models
)
import pytest
from tests.fixtures.models import (
    user,
    stock,
    bank
)


def test_buy_stock(user, stock, bank):
    status = handle.buy_stock(stock_id=stock.id,
                              order_number=10,
                              order_price=10,
                              user_name=user.nickname,
                              order_type=1)
    if status == "购买成功":
        assert user.curreny == 1000 - (10 * 10 * 1.1)
        assert bank.stock_number == 1000


def test_get_stock(stock):
    assert handle.get_stock(stock.id)[0]['id'] == stock.id
    assert handle.get_stock(stock.id)[0]['name'] == stock.name


def test_get_user_stock(user, stock, bank):
    get_user, get_user_stock = handle.get_user_stock(user.nickname)
    assert get_user.id == user.id
    assert get_user_stock[0]['name'] == stock.name
    assert get_user_stock[0]['stock_id'] == stock.id
    assert get_user_stock[0]['stock_number'] == bank.stock_number
