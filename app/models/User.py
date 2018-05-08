# -*- coding: utf-8 -*
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
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
    # posts = relationship('Post', backref='author', lazy='dynamic')
    # stocks = relationship('Bank', backref='user_name', lazy='dynamic')
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
