import matplotlib.pyplot as plt
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd
import numpy as np
import talib as ta
from m_db import m_db2
import datetime
#import seaborn as sns
v_hasbuy_f = 0
v_code_f = 0
v_date_f = 0
v_ccibuy_f = 0
v_pregntbuy_f = 0
v_ccisale_f = 0

v_buyprice = 0
v_saleprice = 0
v_tot_zhenfu = 0
arr_shouyiarr = []
cash =0
df = ''
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
# draw
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
def drawkline(df):
    try:
        lendf = len(df)
    except Exception as e:
        print('ERR:',e)
        return
    maxvol = df['vol'].max()
    minprice = df['low'].min()

    for i in range(lendf):
        if i > 1 and float(df.loc[i]['vol'])>1.4*float(df.loc[i-1]['vol'])\
                and float(df.loc[i-1]['open'])>float(df.loc[i]['close'])\
                and float(df.loc[i]['close'])>float(df.loc[i]['open'])\
                and float(df.loc[i]['open'])>float(df.loc[i-1]['close']):
            v_pregntbuy_f = 1
            saveimg(df.loc[i-1:i+24])
        if i > 1 and float(df.loc[i]['cci']) < 100 and float(df.loc[i]['cci']) > 100:
            v_ccisale_f = 1
        trade(df.loc[i],trandtype='')
        return
def get_canBuy_code(type):
    db = m_db2()
    if type == 'YES':
        db.cur.execute("select code,outstanding from t_all_stickcode where outstanding <  50000 \
                   and (substr(code,1,1)='0' or substr(code,1,1)='6'); ")
    else:
        db.cur.execute("select code,outstanding from t_all_stickcode ;")
    sqlrs = db.cur.fetchall()
    for code in sqlrs:
        # print('pre_data:',code[0])
        df = pre_data(code[0],'W')
        control(df)
    return
def saveimg(df,dfw,date):

    fig = plt.figure()
    ax1 = plt.subplot(211) # 在图表2中创建子图1
    ax2 = plt.subplot(212)  # 在图表2中创建子图1
    # ax1 = plt.subplot(511) # 在图表2中创建子图1
    # ax2 = plt.subplot(512) # 在图表2中创建子图2
    # ax3 = plt.subplot(513)  # 在图表2中创建子图2
    # ax4 = plt.subplot(514)  # 在图表2中创建子图2
    # ax5 = plt.subplot(515)  # 在图表2中创建子图2

    try:
        lendf = len(df)
    except Exception as e:
        return
    maxvol = df['vol'].max()
    minprice = df['low'].min()
    beginindex = df.index.values[0]
    for i in range(lendf):
        df.index.values[i] -= beginindex;
    plt.sca(ax1)
    for i in df.index.values:

        if df.loc[i]['open']<=df.loc[i]['close']:
            color = 'red'
        else:
            color = 'green'
        plt.vlines(i, df.loc[i]['low'], df.loc[i]['high'], linewidth=1,colors=color)
        plt.vlines(i, df.loc[i]['open'], df.loc[i]['close'], linewidth=5, colors=color)
    plt.ylabel(df.loc[df.index.values[0]]['code'])

    df = dfw
    try:
        lendf = len(df)
    except Exception as e:
        return
    maxvol = df['vol'].max()
    minprice = df['low'].min()
    beginindex = df.index.values[0]
    for i in range(lendf):
        df.index.values[i] -= beginindex;
    plt.sca(ax2)
    for i in df.index.values:

        if df.loc[i]['open']<=df.loc[i]['close']:
            color = 'red'
        else:
            color = 'green'
        plt.vlines(i, df.loc[i]['low'], df.loc[i]['high'], linewidth=1,colors=color)
        plt.vlines(i, df.loc[i]['open'], df.loc[i]['close'], linewidth=5, colors=color)
    plt.ylabel(df.loc[df.index.values[0]]['code'])

    # plt.sca(ax2)
    # #plt.plot(df.index, df['diff'])
    # plt.plot(df.index, df['dea'])
    # plt.plot(df.index, df['macd'])
    # plt.hlines(0, 0, len(df) - 1)
    # plt.ylabel('macd')
    #
    # plt.sca(ax3)
    # #vol = (float(df.loc[i]['vol']) / float(maxvol)) * float(minprice) / 4
    # plt.vlines(df.index, '0', df['vol'], linewidth=5, colors='black')
    # plt.plot(df.index,df['volma5'])
    # plt.plot(df.index, df['volma20'])
    # plt.ylabel('vol')
    #
    # plt.sca(ax4)
    # plt.plot(df.index,df['cci'])
    # plt.hlines(100,0,len(df)-1)
    # plt.hlines(-100, 0, len(df)-1)
    # plt.ylabel('cci')
    #
    # plt.sca(ax5)
    # plt.plot(df.index,df['obv'])
    # plt.ylabel('obv')

    plt.savefig('/Users/lgy/PycharmProjects/img/'+df.loc[df.index.values[0]]['code']+' '+df.loc[df.index.values[0]]['date']+date+'.png')
    #plt.close()
    #plt.show()
    plt.close('all')
    return
def trade(df,trandtype=''):
    global v_hasbuy_f
    global v_code_f
    global v_date_f
    global v_ccibuy_f
    global v_pregntbuy_f
    global v_ccisale_f

    global v_buyprice
    global v_saleprice
    global v_tot_zhenfu
    global arr_shouyiarr
    global cash

    #sale
    if 1 == v_hasbuy_f and 1 == v_ccisale_f:
        v_tot_zhenfu += (v_saleprice-v_buyprice)/v_buyprice
        v_hasbuy_f=0
        v_ccibuy_f=0
        arr_shouyiarr.append([df['date'],df['close']])
    #buy
    if 0 == v_hasbuy_f and 1 == v_pregntbuy_f:
        v_hasbuy_f=1
        v_buyprice = df['close'].values
        #arr_shouyiarr.append(v_tot_zhenfu)
    return
def show_canbuy_code(date):
    db = m_db2()
    return db.get_can_buy_code(date)
# db = m_db2()
# allstick = db.get_all_stick()
# for code in allstick['code'].values:
#     print('code:',code)
#     df = pre_data(code)
#     drawkline(df)
def drawDayWeek(code,date,duadays,ktype='D'):
    # code=xxxx date=YYYY-MM-DD
    db = m_db2()
    beginday=datetime.datetime.strptime(date,'%Y-%m-%d')
    endday=beginday + datetime.timedelta(days=duadays)
    beforday=beginday - datetime.timedelta(days=9)
    befordayW = beginday - datetime.timedelta(days=400)
    df = db.pre_data(code,beginday=beforday.strftime('%Y-%m-%d'),endday=endday.strftime('%Y-%m-%d'),ktype=ktype)
    dfw = db.pre_data(code,beginday=befordayW.strftime('%Y-%m-%d'),endday=beforday.strftime('%Y-%m-%d'),ktype='W')
    saveimg(df,dfw,date)
    return
# df = pre_data('600848')
# drawkline(df)





