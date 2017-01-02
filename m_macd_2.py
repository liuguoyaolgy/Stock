import tushare as ts
from m_load_update_data import load
import m_draw
import matplotlib.pyplot as plt
import string
import m_smtp
import datetime

class g():
    a = ''
    b = ''
    c = []

def data_complete():
    # 补全day历史数据
    ld = load()
    # ld.get_stick_hisdata_d(begin_date='2014-01-01',end_date='2016-12-23')
    ld.get_stick_hisdata_d(begin_date='2016-12-01', end_date='2016-12-23')

def run():

    return

#补全历史数据 day
data_complete()


#选股

#买入

#卖出

#打印仓位



