
import tushare as ts
from m_load_update_data import load
import m_draw
import matplotlib.pyplot as plt
import string
import m_smtp
import datetime

price = ''

class cw_dsp():
    def __init__(self):
        self.bishu=0.0
        self.buyamt=0.0
        self.buyprice=0.0
class CW():
    def __init__(self):
        self.canjy = '1'
        self.cw_part = 6
        self.remainder_Amt=100000.0
        self.bili = 0 # 共分六份
        self.jycnt = 0
        self.C1 = cw_dsp()
        self.C2 = cw_dsp()
        self.C3 = cw_dsp()
        self.C4 = cw_dsp()
        self.C5 = cw_dsp()
        self.C6 = cw_dsp()
        self.C7 = cw_dsp()
class CW_ctr():
    def jc(self,ma20,price):
        if 0 == cw.bili:
            print('jc')
            if price <= ma20*p7:
                cw.C7.bishu = int(cw.remainder_Amt / (cw.cw_part - cw.bili) / price / 100)
                cw.C7.buyamt = cw.C7.bishu * 100 * price
                cw.C7.buyprice = price
                cw.bili += 1
                cw.remainder_Amt -= cw.C7.buyamt
            if price <= ma20*p6:
                cw.C6.bishu = int(cw.remainder_Amt / (cw.cw_part - cw.bili) / price / 100)
                cw.C6.buyamt = cw.C6.bishu * 100 * price
                cw.C6.buyprice = price
                cw.bili += 1
                cw.remainder_Amt -= cw.C6.buyamt
            if price <= ma20*p5:
                cw.C5.bishu = int(cw.remainder_Amt / (cw.cw_part - cw.bili) / price / 100)
                cw.C5.buyamt = cw.C5.bishu * 100 * price
                cw.C5.buyprice = price
                cw.bili += 1
                cw.remainder_Amt -= cw.C5.buyamt

            cw.C1.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C1.buyamt=cw.C1.bishu*100*price
            cw.C1.buyprice = price
            cw.bili+=1
            cw.remainder_Amt -= cw.C1.buyamt

            cw.C2.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C2.buyamt=cw.C2.bishu*100*price
            cw.C2.buyprice = price
            cw.bili+=1
            cw.jycnt += 1
            cw.remainder_Amt -= cw.C2.buyamt

            cw.C3.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C3.buyamt=cw.C3.bishu*100*price
            cw.C3.buyprice = price
            cw.bili+=1
            cw.jycnt += 1
            cw.remainder_Amt -= cw.C3.buyamt
            return
        return 
    def buy(self,price,cwno,date):
        if 4 == cw.bili :
            #清仓
            #self.qc(price,date)
            return
        elif 0 == cw.bili and 1 == cwno :
            print('amtdiff:BUY:',cw.bili,date,price)
            cw.C1.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C1.buyamt=cw.C1.bishu*100*price
            cw.C1.buyprice = price
            cw.bili+=1
            cw.remainder_Amt -= cw.C1.buyamt
            return
        elif 1 == cw.bili and 2 == cwno:
            print('amtdiff:BUY:', cw.bili, date, round(price,2))
            cw.C2.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C2.buyamt=cw.C2.bishu*100*price
            cw.C2.buyprice = price
            cw.bili+=1
            cw.remainder_Amt -= cw.C2.buyamt
            return
        elif 2 == cw.bili and 3 == cwno:
            print('amtdiff:BUY:', cw.bili, date, round(price,2))
            cw.C3.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C3.buyamt=cw.C3.bishu*100*price
            cw.C3.buyprice = price
            cw.bili+=1
            cw.remainder_Amt -= cw.C3.buyamt
            return 
        elif 3 == cw.bili and 5 == cwno:
            print('amtdiff:BUY:', cw.bili, date, round(price,2))
            cw.C5.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C5.buyamt=cw.C5.bishu*100*price
            cw.C5.buyprice = price
            cw.bili+=1
            cw.remainder_Amt -= cw.C5.buyamt
            return
        elif 4 == cw.bili and 6 == cwno:
            print('amtdiff:BUY:', cw.bili, date, round(price,2))
            cw.C6.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C6.buyamt=cw.C6.bishu*100*price
            cw.C6.buyprice = price
            cw.bili+=1
            cw.remainder_Amt -= cw.C6.buyamt
            return
        elif 5 == cw.bili and 7 == cwno:
            print('amtdiff:BUY:', cw.bili, date, round(price,2))
            cw.C7.bishu=int(cw.remainder_Amt/(cw.cw_part-cw.bili)/price/100)
            cw.C7.buyamt=cw.C7.bishu*100*price
            cw.C7.buyprice = price
            cw.bili+=1
            cw.remainder_Amt -= cw.C7.buyamt
            return
        else:
            return

    def sale(self,price,cwno,date):
        if 0 == cw.bili:
            return
        if 1 == cw.bili and 1 == cwno:
            return
            print('amtdiff:',cw.bili,date,round(cw.C1.buyprice,2),'->',round(price,2),round(cw.C1.bishu*price*100-cw.C1.buyamt))
            cw.bili -= 1
            cw.remainder_Amt += cw.C1.bishu*price*100
            cw.C1.bishu = 0.0
            cw.C1.buyamt = 0.0
            cw.C1.buyprice = 0.0
            cw.jycnt += 1
            return
        if 2 == cw.bili and 2 == cwno:
            print('amtdiff:',cw.bili,date,round(cw.C2.buyprice,2),'->',round(price,2),round(cw.C2.bishu*price*100-cw.C2.buyamt))
            cw.bili -= 1
            cw.remainder_Amt += cw.C2.bishu*price*100
            cw.C2.bishu = 0.0
            cw.C2.buyamt = 0.0
            cw.C2.buyprice = 0.0
            cw.jycnt += 1
            return
        if 3 == cw.bili and 3 == cwno:
            print('amtdiff:',cw.bili,date,round(cw.C3.buyprice,2),'->',round(price,2),round(cw.C3.bishu*price*100-cw.C3.buyamt))
            cw.bili -= 1
            cw.remainder_Amt += cw.C3.bishu*price*100
            cw.C3.bishu = 0.0
            cw.C3.buyamt = 0.0
            cw.C3.buyprice = 0.0
            cw.jycnt += 1
            return
        if 4 == cw.bili and 5 == cwno:
            print('amtdiff:',cw.bili,date,round(cw.C5.buyprice,2),'->',round(price,2),round(cw.C5.bishu*price*100-cw.C5.buyamt))
            cw.bili -= 1
            cw.remainder_Amt += cw.C5.bishu*price*100
            cw.C5.bishu = 0.0
            cw.C5.buyamt = 0.0
            cw.C5.buyprice = 0.0
            cw.jycnt += 1
            return
        if 5 == cw.bili and 6 == cwno:
            print('amtdiff:',cw.bili,date,round(cw.C6.buyprice,2),'->',round(price,2),round(cw.C6.bishu*price*100-cw.C6.buyamt))
            cw.bili -= 1
            cw.remainder_Amt += cw.C6.bishu*price*100
            cw.C6.bishu = 0.0
            cw.C6.buyamt = 0.0
            cw.C6.buyprice = 0.0
            cw.jycnt += 1
            return
        if 6 == cw.bili and 7 == cwno:
            print('amtdiff:',cw.bili,date,round(cw.C7.buyprice,2),'->',round(price,2),round(cw.C7.bishu*price*100-cw.C7.buyamt))
            cw.bili -= 1
            cw.remainder_Amt += cw.C7.bishu*price*100
            cw.C7.bishu = 0.0
            cw.C7.buyamt = 0.0
            cw.C7.buyprice = 0.0
            cw.jycnt += 1
            return
    def amt(self,price):
        return cw.remainder_Amt+cw.C1.bishu*price*100+cw.C2.bishu*price*100+cw.C3.bishu*price*100+cw.C5.bishu*price*100+cw.C6.bishu*price*100+cw.C7.bishu*price*100
    def amt2(self):
        return cw.remainder_Amt+cw.C1.buyamt+cw.C2.buyamt+cw.C3.buyamt+cw.C5.buyamt+cw.C7.buyamt+cw.C7.buyamt
    def qc(self,price,date):
        # if cw.bili == 0 :
        #     return
        cw.remainder_Amt=self.amt(price)
        print('amtdiff:', cw.bili, date, round(self.amt(price)-self.amt2()),'qqqqqqcccccc')
        cw.bili = 0
        cw.C1.bishu = 0.0
        cw.C1.buyamt = 0.0
        cw.C1.buyprice = 0.0
        cw.C2.bishu = 0.0
        cw.C2.buyamt = 0.0
        cw.C2.buyprice = 0.0
        cw.C3.bishu = 0.0
        cw.C3.buyamt = 0.0
        cw.C3.buyprice = 0.0
        cw.C4.bishu = 0.0
        cw.C4.buyamt = 0.0
        cw.C4.buyprice = 0.0
        cw.C5.bishu = 0.0
        cw.C5.buyamt = 0.0
        cw.C5.buyprice = 0.0
        cw.C6.bishu = 0.0
        cw.C6.buyamt = 0.0
        cw.C6.buyprice = 0.0
        cw.C7.bishu = 0.0
        cw.C7.buyamt = 0.0
        cw.C7.buyprice = 0.0
    def printcw(self):
        print('========== 仓位 ==========')
        print('remain_amt;',round(cw.remainder_Amt))
        print('bili:',cw.bili)
        print('C1-bishu',cw.C1.bishu,'  C1-amt',round(cw.C1.buyamt,2),'   C1-price,',round(cw.C1.buyprice,2))
        print('C2-bishu',cw.C2.bishu,'  C2-amt',round(cw.C2.buyamt,2),'   C2-price,',round(cw.C2.buyprice,2))
        print('C2-bishu',cw.C3.bishu,'  C2-amt',round(cw.C3.buyamt,2),'   C2-price,',round(cw.C3.buyprice,2))
        print('C4-bishu',cw.C4.bishu,'  C4-amt',round(cw.C4.buyamt,2),'   C4-price,',round(cw.C4.buyprice,2))
        print('C5-bishu',cw.C5.bishu,'  C5-amt',round(cw.C5.buyamt,2),'   C5-price,',round(cw.C5.buyprice,2))
        print('C2-bishu',cw.C6.bishu,'  C2-amt',round(cw.C6.buyamt,2),'   C2-price,',round(cw.C6.buyprice,2))
        print('C2-bishu',cw.C7.bishu,'  C2-amt',round(cw.C7.buyamt,2),'   C2-price,',round(cw.C7.buyprice,2))

        print('tot:',round(self.amt2()))
        print('jycnt:',cw.jycnt)
        print('========== === ==========')
        g_listall.append(g_code+' '+str(self.amt2()))
        for lllll in g_listall:
            print(lllll)


def data_complete():
    # 补全day历史数据
    ld = load()
    # ld.get_stick_hisdata_d(begin_date='2014-01-01',end_date='2016-12-23')
    ld.get_stick_hisdata_d(begin_date='2014-01-01', end_date='2016-12-23')


def wangge():
    df = ts.get_k_data('002321',ktype='D')
    return df
#data_complete()


cw = CW()

# p1 = 1.08
# p2 = 1.0533
# p3 = 1.0265
# p5 = 0.9735
# p6 = 0.9467
# p7 = 0.92
# pqc = 0.77

dul = 0.02  # 0.023   0.035
p0 = 1.0 + dul * 3.0 + dul / 2.0
p1 = 1.0 + dul * 2.0 + dul / 2.0
p2 = 1.0 + dul * 1.0 + dul / 2.0
p3 = 1.0 + dul * 0.0 + dul / 2.0
p5 = 1.0 - dul * 0.0 - dul / 2.0
p6 = 1.0 - dul * 1.0 - dul / 2.0
p7 = 1.0 - dul * 2.0 - dul / 2.0
p8 = 1
pqc = 0.75
g_code = ''
g_listall = []

# p1 = 1.18
# p2 = 1.12
# p3 = 1.06
# p5 = 0.94
# p6 = 0.88
# p7 = 0.82
# pqc = 0.77

# p1 = 1.12
# p2 = 1.08
# p3 = 1.04
# p5 = 0.96
# p6 = 0.92
# p7 = 0.88
# pqc = 0.75

def wangge_run(code):
    df = m_draw.pre_data(code,'D')
#    print(df)
    try:
        lendf = len(df)
    except Exception as e:
        print('ERR:',e)
        return
    #for icnt in range(30,lendf):
    df['zfb'] = (df['high'].values.astype('double')-df['MA20'].values.astype('double'))/df['MA20'].values.astype('double')
    df['ffb'] = (df['low'].values.astype('double')-df['MA20'].values.astype('double'))/df['MA20'].values.astype('double')
#    print(df)
#     plt.plot(df.index,df['zfb'],'ro',label="point")
#     plt.plot(df.index,df['ffb'],'ro',label="point")
    #plt.show()


    #print(float(df.loc[lendf-1]['high']),float(df.loc[lendf-1]['low']),float(df.loc[lendf-2]['MA20']))
    ctr = CW_ctr()

    for icnt in range(30,lendf):
        #jiancang
        ma20 = float(df.loc[icnt-2]['MA20'])
        high = float(df.loc[icnt-1]['high'])
        low  = float(df.loc[icnt-1]['low'])
        date = df.loc[icnt-1]['date']
        # cci = float(df.loc[icnt-1]['cci'])
        # cciold = float(df.loc[icnt-2]['cci'])
        price = float(df.loc[icnt-1]['close'])

        # if (cci<100 and cciold > 100 ) :#or (cci<-100 and cciold>-100):
        #     ctr.qc(price,date)
        #     cw.canjy='0'
        # if cci>-100 and cciold<-100:
        #     cw.canjy = '1'
        # if '0' == cw.canjy:
        #     continue
        if 0 == cw.bili:
            ctr.jc(float(df.loc[icnt-2]['MA20']),price)
        if high > ma20*p0 and ma20*p0 > low:
            #ctr.buy(ma20,1)
            ctr.sale(ma20*p1,1,date)
        if high > ma20*p1 and ma20*p1 > low:
            ctr.buy(ma20*p1,1,date)
            ctr.sale(ma20*p1,2,date)
        if high > ma20*p2 and ma20*p2 > low:
            ctr.buy(ma20*p2,2,date)
            ctr.sale(ma20*p2,3,date)
        if high > ma20 * p3 and ma20 * p3 > low:
            ctr.buy(ma20 * p3, 3, date)
            ctr.sale(ma20 * p3, 5, date)
        # if high > ma20 and ma20 > low:
        #     ctr.buy(ma20,3,date)
        #     ctr.sale(ma20,5,date)
        if high > ma20*p5 and ma20*p5 > low:
            ctr.buy(ma20*p5,5,date)
            ctr.sale(ma20*p5,6,date)
        if high > ma20*p6 and ma20*p6 > low:
            ctr.buy(ma20*p6,6,date)
            ctr.sale(ma20*p6,7,date)
        if high > ma20*p7 and ma20*p7 > low:
            ctr.buy(ma20*p7,7,date)
            #ctr.sale(ma20*p6,7,date)
        if high > ma20*pqc and ma20*pqc > low:
         #   print('')
            ctr.qc(ma20*pqc,date)
            #ctr.sale(ma20,1)


    ctr.printcw()
    print(p0,code)

def huice():

    ld = load()
    rs = ld.get_little_stock()
    ctr2 = CW_ctr()
    for code in rs:
        print('')
        print('=======bbbeeegggiiinnn=======')
        ctr2.printcw()
        g_code = code[0]
        wangge_run(code[0])
        ctr2.qc(0,'0000-00-00')
        cw.cw_part = 6
        cw.remainder_Amt = 100000.0
        cw.bili = 0  # 共分六份
        cw.jycnt = 0

#data_complete()
#huice()
#print(g_listall)
#wangge_run('601258')
enddate = datetime.date.today()
df = m_draw.show_canbuy_code(enddate.strftime('%Y-%m-%d'))
str='today code \n'
for ind in df.index:
    str+=df.loc[ind]['date']+" "+df.loc[ind]['code']+"\n"
print(str)
m_smtp.smtp_send(str)



