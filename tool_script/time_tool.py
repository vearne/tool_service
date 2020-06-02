# -*- coding: utf-8 -*-
import time
from datetime import datetime
def datetime2secs(mydate):
    '''
        datetime.datetime 类型 到 自epoch 的秒数
    '''
    return time.mktime(mydate.timetuple())

def secs2datetime(ts):
    tz_utc_8 = timezone(timedelta(hours=8))
    return datetime.fromtimestamp(ts, tz_utc_8)
