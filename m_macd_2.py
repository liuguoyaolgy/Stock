import tushare as ts
from m_load_update_data import load
import m_draw
import matplotlib.pyplot as plt
import string
import m_smtp
import datetime
import talib as ta
from m_db import m_db2
import m_cw
import matplotlib.pyplot as plt
class g():
    a = ''
    b = ''
    c = []

#************
#1.macd 三天是红，第三根是第一根的>4/3倍
#2.0轴上第一个金叉 buy
#3.0轴上第二个金叉买 buy
#
#
#
#**************


def data_complete():
    # 补全day历史数据
    ld = load()
    # ld.get_stick_hisdata_d(begin_date='2014-01-01',end_date='2016-12-23')
    ld.get_stick_hisdata_d(begin_date='2016-12-01', end_date='2016-12-23')

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
    df['MA20'] = ta.MA(df['close'].values.astype('double'), 20)
    df['MA60'] = ta.MA(df['close'].values.astype('double'), 60)
    df['cwbili']=0
    df['pricebili']=0
    return  df
# draw
def run():
    #601999
    #600485
    #601011
    code = '600706'
    df = pre_data(code, ktype='D')
    for icnt in range(30,len(df)):
        #sale
        if 1==in3dHasMacdSaleFlag(df,icnt-1) \
                or 1==diffdown3days(df,icnt-1) \
                or 1==in20DhszshHasSaleFlag(df,icnt-1):
            m_cw.sale(code, float(df.loc[icnt-1]['close']), 1)
            print('S:',df.loc[icnt-1]['date'],m_cw.allamt())
        #buy
        if 1 == in3dHasMacdBuyFlag(df,icnt-1) and 1==diffup3days(df,icnt-1) and 1==ma60up(df,icnt-1):
            m_cw.buy(code, float(df.loc[icnt-1]['close']), 1)
            print('B',df.loc[icnt-1]['date'])
        #用于画图
        df.loc[icnt-1,['cwbili']]=m_cw.allamt()/100000.0
        df.loc[icnt-1,['pricebili']]=float(df.loc[icnt-1]['close'])/float(df.loc[30]['close'])
    return

#最近三天有金叉
def in3dHasMacdBuyFlag(df,daycnt):
    today = daycnt
    yestoday = daycnt - 1
    i_2DAgo = daycnt - 2
    i_3DAgo = daycnt - 3
    if daycnt < 30:
        return 0
    if df.loc[today]['diff']>df.loc[today]['dea'] and df.loc[yestoday]['diff']<df.loc[yestoday]['dea']:
        return 1
    if df.loc[yestoday]['diff'] > df.loc[yestoday]['dea'] and df.loc[i_2DAgo]['diff'] < df.loc[i_2DAgo]['dea']:
        return 1
    if df.loc[i_2DAgo]['diff'] > df.loc[i_2DAgo]['dea'] and df.loc[i_3DAgo]['diff'] < df.loc[i_3DAgo]['dea']:
        return 1
    return 0
#最近三天死叉
def in3dHasMacdSaleFlag(df,daycnt):
    today = daycnt
    yestoday = daycnt - 1
    i_2DAgo = daycnt - 2
    i_3DAgo = daycnt - 3
    if daycnt < 30:
        return 0
    if df.loc[today]['diff']<df.loc[today]['dea'] and df.loc[yestoday]['diff']>df.loc[yestoday]['dea']:
        return 1
    if df.loc[yestoday]['diff'] < df.loc[yestoday]['dea'] and df.loc[i_2DAgo]['diff'] > df.loc[i_2DAgo]['dea']:
        return 1
    if df.loc[i_2DAgo]['diff'] < df.loc[i_2DAgo]['dea'] and df.loc[i_3DAgo]['diff'] > df.loc[i_3DAgo]['dea']:
        return 1
    return 0
#大盘创20日新低
def in20DhszshHasSaleFlag(df,daycnt):
    if float(df.loc[daycnt]['close'])< \
        float(df[daycnt-20:daycnt]['close'].values.astype('double').min()):
        return 1
    return 0
#diff连续三天升高
def diffup3days(df,daycnt):
    if df.loc[daycnt]['diff'] > df.loc[daycnt-1]['diff'] and df.loc[daycnt-1]['diff']>df.loc[daycnt-2]['diff'] \
            and df.loc[daycnt]['macd'] > 4 * df.loc[daycnt - 2]['macd'] / 3 and df.loc[daycnt - 2]['macd']>0:
        return 1
    return 0
#diff连续三天下降
def diffdown3days(df,daycnt):
    if df.loc[daycnt]['diff'] < df.loc[daycnt-1]['diff'] \
            and df.loc[daycnt-1]['diff']<df.loc[daycnt-2]['diff']:
         #   and df.loc[daycnt]['diff']>4*df.loc[daycnt-2]['diff']/3:
        return 1
    return 0
#60日线拐头向上
def ma60up(df,daycnt):
    if df.loc[daycnt]['MA60'] < df.loc[daycnt - 1]['MA60'] \
            and df.loc[daycnt - 1]['MA60'] < df.loc[daycnt - 2]['MA60']:
        return 1
    return 0

db = m_db2()

#补全历史数据 day
#data_complete()

#获取优质小市值
#df = db.getlittlestock('2016-12-13')

#买卖操作
run()

m_cw.cw_print()
plt.plot(df.index,df['cwbili'])
plt.plot(df.index,df['pricebili'])
plt.show()
#打印仓位

# code = '603800'
# df = pre_data(code, ktype='D')
# print(df[0:3]['close'])
# print(df.loc[3]['close'])
# print(df[0:3]['close'].values.astype('double').min())
# print(float(df[0:3]['close'].values.astype('double').min()) >  float(df.loc[3]['close']))



