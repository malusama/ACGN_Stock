import sys
sys.path.append('../')
from models import (
    models
)


session = models.DBSession()
res = session.query(models.Stock).filter(models.Stock.id == 1).first()
print(res)