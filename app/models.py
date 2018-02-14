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
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    posts = relationship('Post', backref='author', lazy='dynamic')

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
    total = Column(Integer, default=None, nullable=False)
    price = Column(Integer, default=None, nullable=False)
    introduction = Column(Text, default='')
    cover = Column(String(255), default=None)


class Bank(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), default=None)
    stock_id = Column(String(255), default=None)
    stock_number = Column(String(255), default=None)


engine = create_engine(
    'postgresql://stock:chensicheng@localhost:5432/dev_stock')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
