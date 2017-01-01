import pymysql
pymysql.install_as_MySQLdb()
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

class m_db2:
    cur = ''
    sqlconn =''
    engine = ''
    def __init__(self):
        self.engine = create_engine('mysql://root:root@127.0.0.1/gupiao?charset=utf8')
        self.sqlconn = pymysql.connect(host='localhost', port=3306,user='root',passwd='root',db='mysql',charset='UTF8')
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
            print('err:',e)
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
# xx=m_db2();
# df=xx.get_test()
# xx.insert_data('t_stick_data_m_test',df.head(20).as_matrix())
# xx.commit()
