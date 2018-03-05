from app.models import (
    models,
)
import pytest


@pytest.fixture(scope='function')
def bank(request, user, stock):
    session = models.DBSession()
    new_bank = models.Bank(
        user_id=user.id, stock_id=stock.id, stock_number=100)

    def delete_bank():
        del_bank = session.query(models.Bank).filter(
            models.Bank.user_id == user.id,
            models.Bank.stock_id == stock.id).first()
        session.delete(del_bank)
        session.commit()
    request.addfinalizer(delete_bank)
    session.add(new_bank)
    session.commit()
    return new_bank
