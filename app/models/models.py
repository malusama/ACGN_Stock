# -*- coding: utf-8 -*
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey
import datetime
import json
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
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    introduction = Column(Text, default='')
    cover = Column(Text, default=None)

    user_id = Column(String(255), default=None)
    works_series = Column(Text, default='')
    release_time = Column(String(255), default=None)
    length_time = Column(String(255), default=None)
    company = Column(String(255), default=None)
    factory = Column(String(255), default=None)
    category = Column(String(255), default=None)
    screenshots = Column(Text, default='')

    banks = relationship('Bank', backref='stock', lazy='dynamic')
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'introduction': self.introduction,
            'cover': self.cover,
            'works_series': self.works_series,
            'release_time': self.release_time,
            'length_time': self.length_time,
            'company': self.company,
            'factory': self.factory,
            'category': self.category,
            'screenshots': self.screenshots
        }


class Bank(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    stock_number = Column(String(255), default=None)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)


class Stock_order(Base):
    __tablename__ = 'stock_order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    stock_number = Column(String(255), default=None)
    order_type = Column(Integer, nullable=False)
    stock_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)


class Stock_apply(Base):
    __tablename__ = 'stock_apply'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    apply_status = Column(Integer, nullable=False)
    stock_name = Column(String(255), default=None)
    cover = Column(String(255), default=None)
    image = Column(String(255), default=None)
    introduction = Column(Text, default='')
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)


class Stock_Magnet(Base):
    __tablename__ = 'stock_magnet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    magnet = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'Magnet': self.magnet,
        }


class Stock_Tag(Base):
    __tablename__ = 'stock_tag'
    id = Column(Integer, primary_key=True)
    tag = Column(String(255), unique=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "tag": self.tag,
        }


scheme = 'postgresql://stock:chensicheng@localhost:5432/dev_stock'
engine = create_engine(scheme, pool_size=100, pool_recycle=1200)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
