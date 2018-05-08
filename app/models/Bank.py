# -*- coding: utf-8 -*
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
import datetime
# 创建对象的基类:
Base = declarative_base()


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
