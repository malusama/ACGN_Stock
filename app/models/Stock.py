# -*- coding: utf-8 -*
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
import datetime
# 创建对象的基类:
Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    introduction = Column(Text, default='')
    cover = Column(Text, default=None)

    user_id = Column(String(255), default=None)
    works_series = Column(Text, default='')
    release_time = Column(DateTime, default=datetime.datetime(1980, 1, 1))
    length_time = Column(String(255), default=None)
    company = Column(String(255), default=None)
    factory = Column(String(255), default=None)
    category = Column(String(255), default=None)
    screenshots = Column(Text, default='')

    # banks = relationship('Bank', backref='stock', lazy='dynamic')
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
