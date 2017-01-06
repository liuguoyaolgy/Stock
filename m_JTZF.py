import m_smtp
import time
import datetime
from m_load_update_data import load

from m_db import m_db2
import tushare as ts
import talib as ta

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
    sqlrs = get_canBuy_code(buytype)
    for code in sqlrs:
        # print('pre_data:',code[0])
        df = pre_data(code[0],'W')
        control(df)
    print('======================show======================')
    df = show_canbuy_code(enddate.strftime('%Y-%m-%d'))
    print(df)
def get_canBuy_code(type):
    db = m_db2()
    if type == 'YES':
        db.cur.execute("select code,outstanding from t_all_stickcode where outstanding <  50000 \
                   and (substr(code,1,1)='0' or substr(code,1,1)='6'); ")
    else:
        db.cur.execute("select code,outstanding from t_all_stickcode ;")
    sqlrs = db.cur.fetchall()
    return sqlrs
def pre_data(stick_code,ktype='D'):
    # ktype in ('D','W','M')
    global df
    db = m_db2()
    try:
        if ktype == 'D':
            df = db.get_data("select * from t_stick_data_d where code = '"+stick_code+"'  and date > '2015-09-01';")#and date>'2015-05-01'
        elif ktype == 'W':
            df = db.get_data("select * from t_stick_data_w where code = '"+stick_code+"'  ;")#and date>'2015-05-01'
        elif ktype == 'M':
            df = db.get_data("select * from t_stick_data_m where code = '" + stick_code + "'  ;")  # and date>'2015-05-01'

    except Exception as e:
        print('ERR:',e)
        return
    df['cci'] = ta.CCI(df['high'].values.astype('double'),df['low'].values.astype('double'),df['close'].values.astype('double'))
    df['diff'],df['dea'],df['macd'] = ta.MACD(df['close'].values.astype('double'),fastperiod=12, slowperiod=26, signalperiod=9)
    df['obv'] = ta.OBV(df['close'].values.astype('double'),df['vol'].values.astype('double'))
    df['volma5']=ta.MA(df['vol'].values.astype('double'),5);
    df['volma20'] = ta.MA(df['vol'].values.astype('double'), 20);
    df['MA20'] = ta.MA(df['close'].values.astype('double'), 5)

    #print(df)
    #i= ta.CDLCONCEALBABYSWALL(df['open'].values.astype('double'),df['high'].values.astype('double'),
    #                       df['low'].values.astype('double'),df['close'].values.astype('double'),)
    #print(i)
    return  df
def control(df):
    db = m_db2()
    if df is None:
        print('is none')
        return
    try:
        lendf = len(df)
        if lendf > 2 and float(df.loc[lendf-1]['vol'])>1.4*float(df.loc[lendf-2]['vol'])\
            and float(df.loc[lendf - 2]['open']) > float(df.loc[lendf-1]['close']) \
            and float(df.loc[lendf-1]['close']) > float(df.loc[lendf-1]['open']) \
            and float(df.loc[lendf-1]['open']) > float(df.loc[lendf - 2]['close']):
            print('can buy:',df.loc[lendf-1]['code'])
            try:
                print("insert ;;;;;;;;;;;;;;;;;;;;;;;;;;",df.loc[lendf-1]['date'],df.loc[lendf-1]['code'])
                db.insert_can_buy_code(df.loc[lendf-1]['date'],df.loc[lendf-1]['code'],'1')
                db.commit()
            except Exception as e:
                print('ERR:',e)
    except Exception as e:
        pre_data('err:',e)
    return
def show_canbuy_code(date):
    db = m_db2()
    return db.get_can_buy_code(date)
def mail_stock(strtime):
    strstr=''
    if '' == strtime :
        enddate = datetime.date.today()
    else :
        enddate = datetime.datetime.strptime(strtime,'%Y-%m-%d')
#    enddate = datetime.date.today() #+ datetime.timedelta(days=1)
    try:
        df = show_canbuy_code(enddate.strftime('%Y-%m-%d'))
    except Exception as e:
        print('ERR:',e)
    strstr=enddate.strftime('%Y-%m-%d')+'\ntotal:'+str(len(df))+'\n'
    if len(df) != 0 :
        for ind in df.index:
            strstr+=df.loc[ind]['code']+"\n"
    print(strstr)
    m_smtp.smtp_send(strstr)
    m_smtp.smtp_send_test('weijin@cupdata.com.cn','jinwei1992','smtp.ym.163.com', strstr)


#补全历史数据 day
#data_complete()

#获取优质小市值
#df = db.getlittlestock('2016-12-13')

#买卖操作
run()


#run('2016-12-28')
# run('')
# mail_stock('')
