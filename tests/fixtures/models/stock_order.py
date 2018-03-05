from app.models import (
    models,
)
import pytest


@pytest.fixture(scope='function')
def stock_order(user, stock):
    session = models.DBSession()
    session.add(models.Stock_order(user_id=user.id,
                                   stock_id=stock.id,
                                   stock_number=20,
                                   stock_type=1,
                                   stock_price=10,
                                   ))
    session.commit()
