import m_smtp
import time
import datetime
from m_load_update_data import load
import m_draw
from m_db import m_db2
import tushare as ts

def run(strtime):
    #refresh database
    if '' == strtime :
        enddate = datetime.date.today()
        begindate = datetime.date.today() - datetime.timedelta(days=13)
    else :
        enddate = datetime.datetime.strptime(strtime,'%Y-%m-%d')
        begindate = enddate - datetime.timedelta(days=13)

    buytype ="YES" # all stock :YES   part stock :NO

    ld = load()
    ld.get_all_stick_inf()
    ld.get_stick_hisdata_w(begindate.strftime('%Y-%m-%d'),enddate.strftime('%Y-%m-%d'),all=buytype)

    #get can buy code
    m_draw.get_canBuy_code(buytype)
    print('======================show======================')
    df = m_draw.show_canbuy_code(enddate.strftime('%Y-%m-%d'))
    print(df)

def test():
    #ld = m_load_update_data.load()
    enddate = datetime.date.today()
    begindate = datetime.date.today() - datetime.timedelta(days=14)
    db = m_db2()
    db.delete_date('t_stick_data_w',enddate.strftime('%Y-%m-%d'),'603900')

def test2():
    rs = ts.get_k_data(code='600275', start='2016-12-01', end='2016-12-14', ktype='W')
    print(rs)

def mail_stock(strtime):
    strstr=''
    if '' == strtime :
        enddate = datetime.date.today()
    else :
        enddate = datetime.datetime.strptime(strtime,'%Y-%m-%d')
#    enddate = datetime.date.today() #+ datetime.timedelta(days=1)
    try:
        df = m_draw.show_canbuy_code(enddate.strftime('%Y-%m-%d'))
    except Exception as e:
        print('ERR:',e)
    strstr=enddate.strftime('%Y-%m-%d')+'\ntotal:'+str(len(df))+'\n'
    if len(df) != 0 :
        for ind in df.index:
            strstr+=df.loc[ind]['code']+"\n"
    print(strstr)
    m_smtp.smtp_send(strstr)
    m_smtp.smtp_send_test('weijin@cupdata.com.cn','jinwei1992','smtp.ym.163.com',strstr)
#run('2016-12-28')
# run('')
# mail_stock('')
