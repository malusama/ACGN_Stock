from app.models import (
    # DBSession,
    base,
    User,
)


def authorization(user, password):
    session = base.DBSession()
    dbuser = session.query(User).filter(
        User.nickname == user).first()
    if dbuser is not None:
        if dbuser.password == password:
            session.close()
            return True
    session.close()
    return False


def register(user, password, email):
    if user is '':
        return False
    if password is '':
        return False
    if email is '':
        return False
    session = base.DBSession()
    userinfo = User(nickname=user,
                    password=password,
                    email=email)
    session.add(userinfo)
    session.commit()
    session.close()
    return True


def get_userid(username):
    if not username:
        raise ValueError
    session = base.base.DBSession()
    user = session.query(User).filter(User.nickname == username).first()
    if not user:
        return "没有用户"
    else:
        return str(user.id)


def get_user_authority(username):
    if not username:
        raise ValueError
    session = base.DBSession()
    user = session.query(User).filter(User.nickname == username).first()
    if not user:
        return "-1"
    else:
        return str(user.authority)
