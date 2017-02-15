# 酒田战法
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
import time
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


# def data_complete():
#     # 补全day历史数据
#     ld = load()
#     # ld.get_stick_hisdata_d(begin_date='2014-01-01',end_date='2016-12-23')
#     ld.get_stick_hisdata_d(begin_date='2016-12-01', end_date='2016-12-23')

def pre_data(stick_code,ktype='D',today=''):
    # ktype in ('D','W','M')
    #today='2010-01-01'
    if '' == today:
        today = datetime.date.today().strftime('%Y-%m-%d')
#        begindate = datetime.date.today() - datetime.timedelta(days=13)

    global df
    db = m_db2()
    try:
        if ktype == 'D':
            df = db.get_data("select * from t_stick_data_d where code = '"+stick_code+"'  and date > '2015-09-01' and date <='"+today+"' order by date asc;")#and date>'2015-05-01'
        elif ktype == 'W':
            df = db.get_data("select * from t_stick_data_w where code = '"+stick_code+"'  ;")#and date>'2015-05-01'
        elif ktype == 'M':
            df = db.get_data("select * from t_stick_data_m where code = '" + stick_code + "'  ;")  # and date>'2015-05-01'

    except Exception as e:
        #print('ERR:',e)
        return
    df['cci'] = ta.CCI(df['high'].values.astype('double'),df['low'].values.astype('double'),df['close'].values.astype('double'))
    df['diff'],df['dea'],df['macd'] = ta.MACD(df['close'].values.astype('double'),fastperiod=12, slowperiod=26, signalperiod=9)
    df['obv'] = ta.OBV(df['close'].values.astype('double'),df['vol'].values.astype('double'))
    df['volma5']=ta.MA(df['vol'].values.astype('double'),5);
    df['volma13'] = ta.MA(df['vol'].values.astype('double'), 13);
    df['volma20'] = ta.MA(df['vol'].values.astype('double'), 20);
    df['volma34'] = ta.MA(df['vol'].values.astype('double'), 34);
    df['MA20'] = ta.MA(df['close'].values.astype('double'), 20)
    df['MA60'] = ta.MA(df['close'].values.astype('double'), 60)
    df['MA5'] = ta.MA(df['close'].values.astype('double'), 5)
    df['MA13'] = ta.MA(df['close'].values.astype('double'), 13)
    df['MA34'] = ta.MA(df['close'].values.astype('double'), 34)
    df['MA89'] = ta.MA(df['close'].values.astype('double'), 89)
    df['MA144'] = ta.MA(df['close'].values.astype('double'), 144)
    df['cwbili']=0
    df['pricebili']=0
    return   df
# draw
def run(code,today):
    #601999
    #600485
    #601011
    #code = '600706'
    #print(code,today)
    df = pre_data(code, ktype='D',today=today)
    try:
        dflen = len(df)-1
        #print(dflen)
        if dflen<10:
            return
    except Exception as e:
        #print(e)
        return
    #print('end pre_Data')
    # for icnt in range(30,len(df)):
        #sale
        # if 1==upGap2Times(df,icnt-1) \
        #         or 1==diffdown3days(df,icnt-1) \
        #         or 1==in20DhszshHasSaleFlag(df,icnt-1):
        #     m_cw.sale(code, float(df.loc[icnt-1]['close']), 1)
        #     print('S:',df.loc[icnt-1]['date'],m_cw.allamt())
        #buy
    #if 1==upGap2Times(df,dflen):
    if 1==gapNotBeFillIn3days(df,dflen) and 1==downGap3Times(df,dflen):
        # m_cw.buy(code, float(df.loc[icnt-1]['close']), 1)
        print('B :  ',today,code)
        m_draw.drawDayWeek(code, today, 60, ktype='D')
        #用于画图
        # df.loc[icnt-1,['cwbili']]=m_cw.allamt()/100000.0
        # df.loc[icnt-1,['pricebili']]=float(df.loc[icnt-1]['close'])/float(df.loc[30]['close'])
    return

# draw
def run2(code,today):
    #601999
    #600485
    #601011
    #code = '600706'
    #print(code,today)
    df = pre_data(code, ktype='D',today=today)
    try:
        dflen = len(df)-1
        #print(dflen)
        if dflen<10:
            return
    except Exception as e:
        #print(e)
        return
    if 1==in5dHasMacdBuyFlag(df,dflen) and 1==vol_canbuyflag(df,dflen) and 1==price_canbuyflag(df,dflen) :
 #           and price_up16per(df,dflen) == 1:
        # m_cw.buy(code, float(df.loc[icnt-1]['close']), 1)
        print('B :  ',today,code)
        try:
            db.insert_can_buy_code(today, code, '2')
            db.commit()
        except Exception as e:
            print('ERR:', e)
    if 1==red_up_throw3MAline(df,dflen):
        print('B :  ',today,code)
        try:
            db.insert_can_buy_code(today, code, '3')
            db.commit()
        except Exception as e:
            print('ERR:', e)
        #m_draw.drawDayWeek(code, today, 60, ktype='D')
        #用于画图
        # df.loc[icnt-1,['cwbili']]=m_cw.allamt()/100000.0
        # df.loc[icnt-1,['pricebili']]=float(df.loc[icnt-1]['close'])/float(df.loc[30]['close'])

    return
#一阳穿三线
def red_up_throw3MAline(df,daycnt):
    today = daycnt
    if float(df.loc[today]['close'])>float(df.loc[today]['MA5']) \
        and float(df.loc[today]['close'])>float(df.loc[today]['MA13']) \
        and float(df.loc[today]['close'])>float(df.loc[today]['MA34']) \
        and float(df.loc[today]['close'])>float(df.loc[today]['MA89']) \
        and float(df.loc[today]['open']) < float(df.loc[today]['MA5']) \
        and float(df.loc[today]['open']) < float(df.loc[today]['MA13']) \
        and float(df.loc[today]['open']) < float(df.loc[today]['MA34']) \
        and float(df.loc[today]['open']) < float(df.loc[today]['MA89']) \
        and float(df.loc[today]['close'])>1.08*float(df.loc[today]['open']):
        return 1
    return 0
#最近5天 有连续两天涨幅大于16%
def price_up16per(df,daycnt):
    today = daycnt
    i_1DAgo = daycnt - 1
    i_2DAgo = daycnt - 2
    i_3DAgo = daycnt - 3
    i_4DAgo = daycnt - 4
    i_5DAgo = daycnt - 5
    if float(df.loc[i_2DAgo]['close']) * 1.11 < float(df.loc[today]['close'] ) \
        or float(df.loc[i_3DAgo]['close']) * 1.11 < float(df.loc[i_1DAgo]['close'] ) \
        or float(df.loc[i_4DAgo]['close']) * 1.11 < float(df.loc[i_2DAgo]['close'] ) \
        or float(df.loc[i_5DAgo]['close']) * 1.11 < float(df.loc[i_3DAgo]['close'] ) :
        return 1
    return 0
#最5天有金叉
def in5dHasMacdBuyFlag(df,daycnt):
    today = daycnt
    yestoday = daycnt - 1
    i_2DAgo = daycnt - 2
    i_3DAgo = daycnt - 3
    i_4DAgo = daycnt - 4
    i_5DAgo = daycnt - 5
    if daycnt < 30:
        return 0
    if df.loc[today]['MA5']>df.loc[today]['MA13'] and df.loc[yestoday]['MA5']<df.loc[yestoday]['MA13']:
        return 1
    if df.loc[yestoday]['MA5'] > df.loc[yestoday]['MA13'] and df.loc[i_2DAgo]['MA5'] < df.loc[i_2DAgo]['MA13']:
        return 1
    if df.loc[i_2DAgo]['MA5'] > df.loc[i_2DAgo]['MA13'] and df.loc[i_3DAgo]['MA5'] < df.loc[i_3DAgo]['MA13']:
        return 1
    if df.loc[i_3DAgo]['MA5'] > df.loc[i_3DAgo]['MA13'] and df.loc[i_4DAgo]['MA5'] < df.loc[i_4DAgo]['MA13']:
        return 1
    if df.loc[i_4DAgo]['MA5'] > df.loc[i_4DAgo]['MA13'] and df.loc[i_5DAgo]['MA5'] < df.loc[i_5DAgo]['MA13']:
        return 1
    return 0
def vol_canbuyflag(df,daycnt):
    today = daycnt
    if df.loc[today]['volma5']>1.8*df.loc[today]['volma34'] \
        and df.loc[today]['volma13']>df.loc[today]['volma34'] :
            return 1
    return 0
def price_canbuyflag(df,daycnt):
    today = daycnt
    if df.loc[today]['MA5'] >  df.loc[today]['MA13'] \
        and df.loc[today]['MA13'] > df.loc[today]['MA34'] \
        and df.loc[today]['MA5'] > df.loc[today]['MA89'] \
        and df.loc[today]['MA5'] > df.loc[today]['MA144'] \
        and float(df.loc[today]['close'])*0.9 < df.loc[today]['MA89'] \
        and float(df.loc[today]['close'])*0.9 < df.loc[today]['MA144'] \
        and float(df.loc[today]['open'])*0.99 > float(df.loc[today]['close']):
        return 1

    return 0
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

#最近两个月 向下跳空三次

#从周线判断近一年的（high-low）/high>50%）分三挡 高档 中档 低档 或者 通过pe判断
def dangWei(df,daycnt):

    return

#向下跳空三次 近一个月 连续下跌（5日线 < 10 日线）下降幅度大于40%
def downGap3Times(df,daycnt):
    if daycnt < 30 :
        return 0
    gapCnt = 0
    for icnt in range(0,30):
        if df.loc[daycnt-30+icnt]['low']>df.loc[daycnt-30+1+icnt]['high']:
            gapCnt +=1
    if gapCnt>=3:
        return 1
    return 0

#连续下跌

#近两个月 跌幅超过40%
def down40percent(df,daycnt):
    if df[daycnt - 30:daycnt]['low'].values.astype('double').min() \
    < 0.6 * df[daycnt - 30:daycnt]['high'].values.astype('double').max():
        return 1
    return 0

#双针探底

#两跳空 买
def upGap2Times(df,daycnt):
    if df.loc[daycnt]['low'] > df.loc[daycnt - 1]['high'] \
            and df.loc[daycnt - 1]['low'] > df.loc[daycnt - 2]['high']\
            and float(df.loc[daycnt - 2]['low']) > df[daycnt - 23:daycnt - 3]['high'].values.astype('double').max()\
            and df[daycnt - 23:daycnt - 3]['low'].values.astype('double').min()>0.8*df[daycnt - 23:daycnt - 3]['high'].values.astype('double').max():
        return 1
    return 0

#缺口三天不补 买
def gapNotBeFillIn3days(df,daycnt):
    if df[daycnt-2:daycnt+1]['low'].values.astype('double').min() > float(df.loc[daycnt-3]['high'])\
            and float(df.loc[daycnt]['close'])<1.04*float(df.loc[daycnt-3]['high'])\
            and df[daycnt-1:daycnt+1]['high'].values.astype('double').max()<float(df.loc[daycnt-2]['close'])\
            and float(df.loc[daycnt-3]['high'])>1.06*float(df.loc[daycnt-3]['low']) :
        #print('min:',df[daycnt-2:daycnt]['low'].values.astype('double').min(),'high:',df.loc[daycnt-3]['high'])
        return 1
    return 0

#法6 脱出盘整 跳空向下出三只连续线 买

#法7 下切线 买
def F7_xiaQieXian(df,daycnt):
    if df[daycnt-2:daycnt+1]['low'].values.astype('double').min() > float(df.loc[daycnt-3]['high'])\
            and float(df.loc[daycnt]['close'])<1.04*float(df.loc[daycnt-3]['high'])\
            and df[daycnt-1:daycnt+1]['high'].values.astype('double').max()<float(df.loc[daycnt-2]['close'])\
            and float(df.loc[daycnt-3]['high'])>1.06*float(df.loc[daycnt-3]['low']) :
        #print('min:',df[daycnt-2:daycnt]['low'].values.astype('double').min(),'high:',df.loc[daycnt-3]['high'])
        return 1
    return

#法10 怀抱线 买
def F10_huaiBaoXian(df,daycnt):

    return

#法16 上窜连续星线 买

#法19 反拖线 买

#法21 下阻线（金针探底）下跌一个月 当日成交量放大
def F21_xiaZuXian(df,daycnt):

    return

#法23 母子形态 外孕十字星 成交量放大 翌日确认（高开收阳，成交量放大）
def F23_muZiXingTai(df,daycnt):

    return

#法41 红三兵 买

#法43 川子三黑 翌日高开收阳 买

#法53 逆袭线 买

#法54 回落再涨买 红三兵要强劲

#法59 下十字 买
def F59_xiaShiZi(df,daycnt):

    return

#法62 u字线 买

#法63 擎天一柱 买
def F63_qingTianYiZhu(df,daycnt):

    return

#法65 锅底 买

#w底部
def W_bottom(df,daycnt):

    return


#回测 每天回测所有股票
def huiCeMoniDay():
    #近一年回测
    for cnt in range(1,30):
        currentday = datetime.date.today() - datetime.timedelta(days=30-cnt)
        strcurrentday = currentday.strftime('%Y-%m-%d')
        print(time.asctime( time.localtime(time.time()) ),'currentday:',currentday)
        coderslt = db.getXiaoShiZhiStock()
        for code in coderslt['code']:
         #   run(code,strcurrentday)
            run2(code,strcurrentday)

    return
#回测 指定时间段回测所有股票 不采取
def huice():

    return
def runtoday():
    currentday = datetime.date.today()
    strcurrentday = currentday.strftime('%Y-%m-%d')
    print(time.asctime(time.localtime(time.time())), 'currentday:', currentday)
    coderslt = db.getXiaoShiZhiStock()
    for code in coderslt['code']:
        #   run(code,strcurrentday)
        run2(code, strcurrentday)
    return

################################
db = m_db2()
ld = load()
def m_run():

#补全历史数据 day
#ld.data_complete(beginday='2015-06-01',endday='2017-02-14',ktype='D')
    enddate = datetime.date.today()
    begindate = datetime.date.today() - datetime.timedelta(days=7)
    ld.data_complete(beginday=begindate.strftime('%Y-%m-%d'),endday=enddate.strftime('%Y-%m-%d'),ktype='D')

#m_draw.drawDayWeek('000672','2016-12-30',10,ktype='D')
#huiCeMoniDay()
    runtoday()

#获取优质小市值
#df = db.getlittlestock('2016-12-13')

#买卖操作
# run()
#
# m_cw.cw_print()
# plt.plot(df.index,df['cwbili'])
# plt.plot(df.index,df['pricebili'])
# plt.show()
#打印仓位

# code = '603800'
# df = pre_data(code, ktype='D')
# print(df[0:3]['close'])
# print(df.loc[3]['close'])
# print(df[0:3]['close'].values.astype('double').min())
# print(float(df[0:3]['close'].values.astype('double').min()) >  float(df.loc[3]['close']))





