# -*- coding: utf-8 -*
from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
import datetime
# 创建对象的基类:
Base = declarative_base()


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
