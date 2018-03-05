from app.models import (
    models
)
import pytest


@pytest.fixture(scope='module')
def user(request):
    session = models.DBSession()
    new_user = models.User(nickname='test_admin',
                           password='chensicheng',
                           email='test@test.com',
                           currency=1000)

    def delete_user():
        del_user = session.query(models.User).filter(
            models.User.nickname == 'test_admin').first()
        session.delete(del_user)
        session.commit()
        session.close()
    request.addfinalizer(delete_user)
    session.add(new_user)
    session.commit()
    return new_user
