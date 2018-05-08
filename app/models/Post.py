from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
import datetime

Base = declarative_base()


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
