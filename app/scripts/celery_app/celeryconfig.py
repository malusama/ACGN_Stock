# -*- coding: utf-8 -*-
from celery.schedules import crontab
from datetime import timedelta


# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'celery_app.DMM',
    'celery_app.DMM_Storage',
    'celery_app.bangumi_Storage'
)

# schedules
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'celery_app.DMM.get_anime_link',
        'schedule': timedelta(seconds=30)       # 每 30 秒执行一次
        # 'args': (5, 8)                           # 任务函数参数
    }
}
