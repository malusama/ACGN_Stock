# -*- coding: utf-8 -*
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
# 创建对象的基类:
Base = declarative_base()


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
