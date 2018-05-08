# -*- coding: utf-8 -*
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
import datetime
# 创建对象的基类:
Base = declarative_base()


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
