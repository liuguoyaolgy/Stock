
import configparser


class cw_dsp():
    def __init__(self):
        self.code=''
        self.bishu = 0.0
        self.buyamt = 0.0
        self.buyprice = 0.0

class CW():
    def __init__(self):
        self.canjy = '1'
        self.cw_part = 6
        self.remainder_Amt = 100000.0
        self.stockcnt=0
        self.stockcnt_max = 4
        self.bili = 0  # 共分六份
        self.jycnt = 0
        self.C = []


cww = CW()
cwdsp = cw_dsp()
#买入

def allamt():
    tmpamt = cww.remainder_Amt
    for i in range(cww.stockcnt):
        tmpamt+=cww.C[i-1].buyamt
    return tmpamt

# input:股票代码 价格 买入总价格比例
def buy(code,price,bili):
    for i in range(cww.stockcnt):
        if cww.C[i-1].code == code:
            return
    if int(bili*allamt()/price/100)*price > cww.remainder_Amt or int(bili*allamt()/price/100)*price < 1:
        return
    if cww.stockcnt_max > cww.stockcnt:
        cwdsp = cw_dsp()
        cwdsp.code = code
        cwdsp.buyprice = price
        cwdsp.bishu = int(bili*allamt()/price/100)
        cwdsp.buyamt = price*cwdsp.bishu*100
        cww.C.append(cwdsp)
        cww.stockcnt +=1
        cww.bili += bili
        cww.remainder_Amt -= cwdsp.buyamt


#input:股票代码 价格 该股票持仓比例
def sale(code,price,bili):
    for i in range(cww.stockcnt):
        if cww.C[i-1].code == code:
            if int(bili*cww.C[i-1].bishu) > 0:
                cww.remainder_Amt += int(bili*cww.C[i-1].bishu)*price*100
                cww.C[i - 1].buyamt = cww.C[i-1].buyamt*(1-int(bili*cww.C[i-1].bishu)/cww.C[i-1].bishu)
                cww.C[i - 1].bishu -= int(bili*cww.C[i-1].bishu)
                if 0== cww.C[i - 1].bishu:
                    del cww.C[i - 1]
                    cww.stockcnt -=1
            else:
                return


def cw_read():
    cf = configparser.ConfigParser()
    cf.read('/home/lgy/PycharmProjects/Stock/cw.txt')
    cww.stockcnt = int(cf.get('cw', 'stockcnt'))
    cww.remainder_Amt = float(cf.get('cw', 'remainder_Amt'))
    cww.bili = float(cf.get('cw', 'bili'))
    for i in range(cww.stockcnt):
        strstr = 'cwdsp'+str(i)
        cwdsp = cw_dsp()
        cwdsp.code = cf.get(strstr, 'code')
        cwdsp.buyprice = float(cf.get(strstr, 'buyprice'))
        cwdsp.bishu = int(cf.get(strstr, 'bishu'))
        cwdsp.buyamt = float(cf.get(strstr, 'buyamt'))
        cww.C.append(cwdsp)
    return
def cw_save():
    strstr = '[cw]\nstockcnt='+str(cww.stockcnt)+'\nremainder_Amt='+str(cww.remainder_Amt)+'\nbili='+str(cww.bili)+'\n'
    for i in range(cww.stockcnt):
        strstr +='[cwdsp'+str(i)+']\ncode='+str(cww.C[i-1].code)+'\nbuyprice='+str(cww.C[i-1].buyprice)\
                 +'\nbishu='+str(cww.C[i-1].bishu)+'\nbuyamt='+str(cww.C[i-1].buyamt)+'\n'
    file_object = open('/home/lgy/PycharmProjects/Stock/cw.txt', 'w')
    file_object.write(strstr)
    file_object.close()
    return

def cw_print():
    strstr ='stockcnt'+str(cww.stockcnt)+'\n'\
    'remainder_amt:'+str(cww.remainder_Amt)+'\n'\
    'code\tbishu\tbuyamt\tbuyprice\n'

    print('stockcnt:',cww.stockcnt)
    print('remaimder_amt:',cww.remainder_Amt)
    for  i in range(cww.stockcnt):
        strstr +=''+  str(cww.C[i-1].code) +'\t'+ str(cww.C[i-1].bishu)+'\t\t'+ str(cww.C[i-1].buyamt)+'\t'+ str(cww.C[i-1].buyprice)+'\n'
        print(cww.C[i-1].code,cww.C[i-1].bishu,cww.C[i-1].buyamt,cww.C[i-1].buyprice)
    return  strstr
# cw_read()
# cw_print()
# buy('000222',19,0.33)
# buy('000220',18,0.33)
# buy('000221',17,0.33)
# cw_print()
# cw_save()
# sale('000222',18,0.5)
# sale('000220',17,0.5)
# sale('000221',16,1)
#
# cw_print()
# cw_save()

#卖出

#清仓

#满仓

#打印仓位