from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey
import datetime

# 创建对象的基类:
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(255), unique=True)
    password = Column(String(255))
    email = Column(String(255), unique=True)
    currency = Column(String(255), default='1000')
    authority = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    posts = relationship('Post', backref='author', lazy='dynamic')
    stocks = relationship('Bank', backref='user_name', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    introduction = Column(Text, default='')
    cover = Column(String(255), default=None)
    banks = relationship('Bank', backref='stock', lazy='dynamic')


class Bank(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    stock_number = Column(String(255), default=None)


class Stock_order(Base):
    __tablename__ = 'stock_order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    stock_number = Column(String(255), default=None)
    order_type = Column(Integer, nullable=False)
    stock_price = Column(Integer, nullable=False)


class Stock_apply(Base):
    __tablename__ = 'stock_apply'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    apply_status = Column(Integer, nullable=False)
    stock_name = Column(String(255), default=None)
    cover = Column(String(255), default=None)
    image = Column(String(255), default=None)
    introduction = Column(Text, default='')


engine = create_engine(
    'postgresql://stock:chensicheng@localhost:5432/dev_stock')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
