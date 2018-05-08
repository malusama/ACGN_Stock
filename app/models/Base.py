from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

scheme = 'postgresql://stock:chensicheng@localhost:5432/dev_stock'
engine = create_engine(scheme, pool_size=100, pool_recycle=1200)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
