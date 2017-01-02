import matplotlib.pyplot as plt
import tushare as ts
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import time
import datetime
from m_db import m_db2
#from ConfigParser import SafeConfigParser
import configparser

class load:
    engine =''
    sqlconn =''
    cur =''
    db = ''
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read('/home/lgy/PycharmProjects/Stock/stock.init')
        usr = cf.get('db','db_user')
        pwd = cf.get('db', 'db_pass')
        # self.engine = create_engine('mysql://root:root@127.0.0.1/gupiao?charset=utf8')
        # self.sqlconn = pymysql.connect(host='localhost', port=3306,user='root',passwd='root',db='mysql',charset='UTF8')
        self.engine = create_engine('mysql://'+usr+':'+pwd+'@127.0.0.1/gupiao?charset=utf8')
        self.sqlconn = pymysql.connect(host='localhost', port=3306,user=usr,passwd=pwd,db='mysql',charset='UTF8')
        self.cur = self.sqlconn.cursor()
        self.cur.execute("use gupiao;")
        self.db = m_db2()
    def __del__(self):
        self.sqlconn.close()
    def get_all_stick_inf(self):
        try:
            df = ts.get_stock_basics()
        except Exception as e:
            print('Err:',e)
            return

        cnt = 0;
        print('begin====== 股票数量不同则 全量更新所有股票基本面信息 ===============')
        while cnt < 3:
            try:
                self.cur.execute("select count(*) from t_all_stickcode; ")
                rs = self.cur.fetchall()
                print('rs:',rs[0][0],len(df))
                if rs[0][0] == len(df) :
                    break
                print('delete')
                self.cur.execute("delete from t_all_stickcode; ")
                self.sqlconn.commit()
                print('insert')
                df.to_sql('t_all_stickcode',self.engine,if_exists='append')
            except:
                print('err')
                df.to_sql('t_all_stickcode',self.engine,if_exists='append')
            cnt += 1;

        #df = ts.get_
        self.sqlconn.commit()
        return

    def get_stick_hisdata_w(self,begin_date,end_date,all='YES'):

        if all == 'YES':
            print('all stock ...........')
            self.cur.execute(
                "select code,outstanding from t_all_stickcode ;")
        else:
            print('part stock ........................')
            self.cur.execute("select code,outstanding from t_all_stickcode where outstanding <  50000 and (substr(code,1,1)='0' or substr(code,1,1)='6'); ;")
        #self.cur.execute("select code,outstanding from t_all_stickcode  a where not EXISTS (select * from t_stick_data_w where code = a.code);")
        sqlrs = self.cur.fetchall();
        # self.cur.execute("delete from t_stick_data_w")
        #self.sqlconn.commit()
        for code in sqlrs:
            print(code[0]+'_w' ,begin_date,end_date)
            try:
                rs = ts.get_k_data(code=code[0],start=begin_date,end=end_date,ktype='W')
            except Exception as e:
                print('ERR:',e)
            self.db.delete_date('t_stick_data_w',begin_date,code[0])
            self.db.insert_data('t_stick_data_w',rs.as_matrix())
            self.db.commit()
        return
    def get_stick_hisdata_d(self,begin_date,end_date):

        # cur.execute("select code,outstanding from t_all_stickcode where outstanding <  50000 and (substr(code,1,1)='0' or substr(code,1,1)='6'); ;")
        self.cur.execute("select code,outstanding from t_all_stickcode  ;")
        sqlrs = self.cur.fetchall();
        # self.cur.execute("delete from t_stick_data_d")
        self.sqlconn.commit()
        for code in sqlrs:
            print(code[0]+'_d' )
            try:
                rs = ts.get_k_data(code=code[0],start=begin_date,end=end_date,ktype='D')
            except Exception as e:
                print('ERR:',e)
                continue
            # rs.to_sql('t_stick_data_d',self.engine,if_exists='replace',index=False);
            self.db.delete_date('t_stick_data_d',end_date,code[0])
            self.db.insert_data('t_stick_data_d',rs.as_matrix())
        self.sqlconn.commit()
        return
    def get_stick_hisdata_m(self,begin_date,end_date):

        # cur.execute("select code,outstanding from t_all_stickcode where outstanding <  50000 and (substr(code,1,1)='0' or substr(code,1,1)='6'); ;")
        self.cur.execute("select code,outstanding from t_all_stickcode a where not EXISTS (select * from t_stick_data_M where code = a.code);")
        sqlrs = self.cur.fetchall();
        # self.cur.execute("delete from t_stick_data_m")
        self.sqlconn.commit()
        for code in sqlrs:
            print(code[0] )
            rs = ts.get_k_data(code=code[0],start=begin_date,end=end_date,ktype='M')
            self.db.delete_date('t_stick_data_M',end_date,code[0])
            self.db.insert_data('t_stick_data_M',rs.as_matrix())
            self.sqlconn.commit()
        return
    def get_stick_hisdata_add_m(self):

        # cur.execute("select code,outstanding from t_all_stickcode where outstanding <  50000 and (substr(code,1,1)='0' or substr(code,1,1)='6'); ;")
        # cur.execute("select code,outstanding from t_all_stickcode  ;")
        # sqlrs = cur.fetchall();
        # cur.execute("delete from t_stick_data_m")
        # sqlconn.commit()
        # for code in sqlrs:
        #     print(code[0]+'_m' )
        #     rs = ts.get_k_data(code=code[0],start='2001-01-01',end='2016-12-31',ktype='M')
        #     rs.to_sql('t_stick_data_m_test',engine,if_exists='append');
        rs = ts.get_k_data(code='600848',start='2013-01-01',end='2014-01-01',ktype='M')
        rs.to_sql('t_stick_data_m_test',self.engine,if_exists='replace',index=False);
        self.sqlconn.commit()
        return
    def get_little_stock(self):
        self.cur.execute("select code from t_all_stickcode where liquidassets <  70000  and liquidassets >  60000 and (substr(code,1,1)='0' or substr(code,1,1)='6') ;")
        rs = self.cur.fetchall();
        return rs

# enddate = datetime.date.today()
# begindate = datetime.date.today() - datetime.timedelta(days=336)
#
# ld = load()
# ld.get_all_stick_inf()
# ld.get_stick_hisdata_w(begindate.strftime('%Y-%m-%d'),enddate.strftime('%Y-%m-%d'),all='YES')

# ld.get_stick_hisdata_w()
#get_stick_hisdata_d()
#get_stick_hisdata_w()
#get_stick_hisdata_m()
#get_stick_hisdata_add_m()
# rs = ts.get_k_data(code='600848', start='2016-06-01', end='2017-01-01', ktype='w')
# print(rs)

# cf = configparser.ConfigParser()
# cf.read('stock.init')
# usr = cf.get('db','db_user')
# pwd = cf.get('db', 'db_pass')
# print(usr,pwd)

