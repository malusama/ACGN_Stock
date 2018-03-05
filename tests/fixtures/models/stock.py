from app.models import (
    models,
)
import pytest


@pytest.fixture(scope='module')
def stock(request):
    session = models.DBSession()
    new_stock = models.Stock(name='test_stock')

    def delete_stock():
        del_stock = session.query(models.Stock).filter(
            models.Stock.name == 'test_stock').first()
        session.delete(del_stock)
        session.commit()
    request.addfinalizer(delete_stock)
    session.add(new_stock)
    session.commit()
    return new_stock
