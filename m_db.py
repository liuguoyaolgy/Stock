import pymysql
pymysql.install_as_MySQLdb()
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import configparser
import datetime
import talib as ta

class m_db2:
    cur = ''
    sqlconn =''
    engine = ''
    def __init__(self):
        cf = configparser.ConfigParser()
        # cf.read('/home/lgy/PycharmProjects/Stock/stock.init')
        cf.read('stock.init')
        usr = cf.get('db','db_user')
        pwd = cf.get('db', 'db_pass')
        # self.engine = create_engine('mysql://root:root@127.0.0.1/gupiao?charset=utf8')
        # self.sqlconn = pymysql.connect(host='localhost', port=3306,user='root',passwd='root',db='mysql',charset='UTF8')
        self.engine = create_engine('mysql://'+usr+':'+pwd+'@127.0.0.1/gupiao?charset=utf8')
        self.sqlconn = pymysql.connect(host='localhost', port=3306,user=usr,passwd=pwd,db='mysql',charset='UTF8')
        self.cur = self.sqlconn.cursor()
        self.cur.execute("use gupiao;")
        # cur.execute("select * from t_stick_data_w where code ='002349';")
        # sqlrs=np.array(cur.fetchall())
        # df = pd.DataFrame(sqlrs,columns=['ind','date','open','close','high','low','vol','code'])
    def __del__(self):
        self.sqlconn.commit()
        self.sqlconn.close()
    def commit(self):
        self.sqlconn.commit()
        return
    def get_test(self):
        self.cur.execute("select date,open,close,high,low,vol,code from t_stick_data_m_test ;")
        return pd.DataFrame(np.array(self.cur.fetchall()),columns=['date','open','close','high','low','vol','code'])
    def insert_test(self,columns):
        columns.to_sql('t_stick_data_m_test',self.engine,if_exists='replace',index=False)
        return
    def get_test_2(self):
        return pd.read_sql_query('select date,open,close,high,low,vol,code '
                                 'from (select * from t_stick_data_m_test order by date desc limit 15) a '
                                 'order by date asc;',self.sqlconn)


    def insert_data(self,tablename,clmn):
        lenr = len(clmn)
        if lenr == 0:
            print('go')
            return
        lenc = len(clmn[0])
        sqlline =''
        for indr in range(lenr):
            #print(np.array_str(clmn[indr]).replace('[','').replace(']','').replace(' ',','))
            sqlline = np.array_str(clmn[indr]).replace('[','').replace(']','').replace(' ',',')
            sql = 'insert into '+tablename+' VALUES ('+ sqlline+');'
            #print(sql)
            try:
                # print('insert into '+tablename+' VALUES ('+ sqlline+');')
                self.cur.execute(sql)
            except Exception as e:
                print('err:',e)
            sqlline=''
        return
    def get_data(self,sql):
        try:
            self.cur.execute(sql)
        except Exception as e:
            print('err:',e)
        return pd.DataFrame(np.array(self.cur.fetchall()),columns=['date','open','close','high','low','vol','code'])

    def get_all_stick(self):
        try:
            self.cur.execute("select code from t_all_stickcode where liquidassets <  70000  and (substr(code,1,1)='0' or substr(code,1,1)='6');")
        except Exception as e:
            #print('err:',e)
            return pd.DataFrame(np.array(self.cur.fetchall()), columns=['code'])
        return pd.DataFrame(np.array(self.cur.fetchall()),columns=['code'])
    def delete_date(self,table,date,code):
        #print('dateeeeeeeeeeee',date)
        sql = ''
        sql = "delete from "+table+" where date >= '"+date+"' and code='"+code+"';"
        #print(sql)
        try:
            self.cur.execute(sql)
            self.commit()
        except Exception as e:
            print('err:', e)
        return
    def insert_can_buy_code(self,date,code,buytype):
        self.cur.execute("insert into t_stick_canbuy values('"+date+"','"+code+"','"+buytype+"');")
        self.commit()
    def get_can_buy_code(self,date):
        df = ''
        try:
            self.cur.execute("select date,code,buytype from t_stick_canbuy where date='"+date+"';")
        except Exception as e:
            print('err:',e)
        try:
            df = pd.DataFrame(np.array(self.cur.fetchall()), columns=['date', 'code', 'buytype'])
        except Exception as e:
            print('Err:', e)
        return df
    def getlittlestock(self,date):
        df = ''
        try:
            sqlstr="select * from ( \
                select a.code,pe,totals,b.close,b.close*a.totals as totprice \
                from t_all_stickcode a  \
                , t_stick_data_d b \
                where  b.date ='"+date+"' and a.code=b.code \
                and pe>5 and pe<200 and b.close*a.totals  < 100) c \
                order by c.totprice asc"
            print(sqlstr)
            self.cur.execute(sqlstr)
            df = pd.DataFrame(np.array(self.cur.fetchall()), columns=['code', 'pe', 'totals','close','totprice'])
        except Exception as e:
            print('Err:', e)
        return df
#获取小市值股票
    def getXiaoShiZhiStock(self):
        try:
            sqlstr=" select a.code,pe,totals \
                from t_all_stickcode a  \
                where   pe>5 and pe<200 and a.totals  < 10 and pe>5 and pe<200 and timetomarket < 20140901;"
            #print(sqlstr)
            self.cur.execute(sqlstr)
            df = pd.DataFrame(np.array(self.cur.fetchall()), columns=['code', 'pe', 'totals'])
        except Exception as e:
            print('Err:', e)
            return None
        return df

    def pre_data(self,stick_code, ktype='D', beginday='',endday=''):
        # ktype in ('D','W','M')
        # today='2010-01-01'
        if '' == beginday:
            begindaytmp = datetime.date.today() - datetime.timedelta(days=13)
            beginday = begindaytmp.strftime('%Y-%m-%d')
        if '' == endday:
            endday = datetime.date.today().strftime('%Y-%m-%d')

        df =''
        print(beginday,endday)
        try:
            if ktype == 'D':
                df = self.get_data(
                    "select * from t_stick_data_d \
                    where code = '" + stick_code + "'  and date > '"+beginday+"' \
                    and date <='" + endday + "' order by date asc;")  # and date>'2015-05-01'
            elif ktype == 'W':
                df = self.get_data(
                    "select * from t_stick_data_w \
                    where code = '" + stick_code + "'  and date > '"+beginday+"' \
                    and date <='" + endday + "' order by date asc;")  # and date>'2015-05-01'
            elif ktype == 'M':
                df = self.get_data(
                    "select * from t_stick_data_m \
                    where code = '" + stick_code + "'  and date > '"+beginday+"' \
                    and date <='" + endday + "' order by date asc;")  # and date>'2015-05-01'

        except Exception as e:
            # print('ERR:',e)
            return
        df['cci'] = ta.CCI(df['high'].values.astype('double'), df['low'].values.astype('double'),
                           df['close'].values.astype('double'))
        df['diff'], df['dea'], df['macd'] = ta.MACD(df['close'].values.astype('double'), fastperiod=12, slowperiod=26,
                                                    signalperiod=9)
        df['obv'] = ta.OBV(df['close'].values.astype('double'), df['vol'].values.astype('double'))
        df['volma5'] = ta.MA(df['vol'].values.astype('double'), 5);
        df['volma20'] = ta.MA(df['vol'].values.astype('double'), 20);
        df['MA20'] = ta.MA(df['close'].values.astype('double'), 20)
        df['MA60'] = ta.MA(df['close'].values.astype('double'), 60)
        df['cwbili'] = 0
        df['pricebili'] = 0
        return df
# xx=m_db2();
# df=xx.pre_data('000157',ktype='W')
# print(df)
# xx.insert_data('t_stick_data_m_test',df.head(20).as_matrix())
# xx.commit()
