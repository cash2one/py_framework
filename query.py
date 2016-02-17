#!coding:utf8
import os,glob
import sys
import sqlite3


def init_db():
    conn=sqlite3.connect('wise_share.db')
    #conn.execute(''' drop table if exists refernum''')
    return conn

def query_db(c,sql):
    cur=c.execute(sql)
    for row in cur:
        yield row

def compare_pv_sql(se,date1,date2,dims):
    for dim in dims:
        sql='''
        select 
            a.date,b.date,a.se,a.dim,a.vlu,a.pv,b.pv,b.pv*1.0/a.pv-1
        from 
        (
          select * 
          from refernum 
          where
           se='%s' 
          and date ='%s' 
          and dim='%s' 
        ) a
        join 
        (
          select * 
          from refernum 
          where
          se='%s' 
          and date ='%s' 
          and dim='%s' 
        ) b
        on a.dim=b.dim
        and a.vlu=b.vlu
        and a.se=b.se
        order by 7 desc
        ;
        '''%(se,date1,dim,se,date2,dim)
        yield sql
    
def compare_share_sql(se,date1,date2,dims):
    for dim in dims:
        sql='''
        select 
            a.date,b.date,a.se,a.dim,a.vlu,a.share,b.share,b.share*1.0/a.share-1
        from 
        (
          select * 
          from refernum 
          where
           se='%s' 
          and date ='%s' 
          and dim='%s' 
        ) a
        join 
        (
          select * 
          from refernum 
          where
          se='%s' 
          and date ='%s' 
          and dim='%s' 
        ) b
        on a.dim=b.dim
        and a.vlu=b.vlu
        and a.se=b.se
        order by 7 desc
        ;
        '''%(se,date1,dim,se,date2,dim)
        yield sql

def browser_change():
    se,brw='baidu','qq'
    se,brw='sogou','qq'
    se,brw='sm','uc'
    for se,brw in [('sogou','qq'),('sm','uc')]:
        sql='''
        select  '%s','%s',a.date, a.pv1, b.pv2 , b.pv2*1.0/ a.pv1*1.0
        from 
        ( select date,sum(pv) pv1 
            from refernum 
            where dim='浏览器' and se='%s' 
            group by date 
        ) a
        join 
        ( select date,sum(pv) pv2 
            from refernum 
            where dim='浏览器' and se='%s' and vlu='%s' 
            group by date 
        ) b
        on a.date=b.date
        order by a.date desc
        limit 10 
        '''%(se,brw,se,se,brw)
        yield sql

def draft():
    sql="select * from refernum where  dim='浏览器'  and se='%s' "%(se)
    #sql="""
    #    select se,vlu,avg(pv) from refernum 
    #    where dim='需求'  
    #and date >='20150830' and date<='20150926'
    #    group by se,vlu 
    #    """
    #sql="select *  from refernum  where date='20151101' and dim='数据源'"
    #sql="select *  from clickprob  where date='20151101' "
    #sql="select distinct dim  from refernum  where date='20151101'"
        #and date >='20150927' and date<='20151031'
    #print sql
    yield sql

def main():
    c=init_db()
    ags=sys.argv
    agl=len(sys.argv)
    se=ags[1] if agl>1 else 'sogou'
    date1=ags[2] if agl>2 else '20151115'
    date2=ags[3] if agl>3 else '20151122'
    dims='数据源,地域,操作系统,手机,浏览器,需求,城市,省份划档'.split(',')
    dims='操作系统,手机,浏览器'.split(',')
    sqls= compare_share_sql(se,date1,date2,dims)
    #sqls= compare_pv_sql(se,date1,date2,dims)
    if agl>4 and ags[4]=='pv':
        sqls= compare_pv_sql(se,date1,date2,dims)
    #sqls= browser_change()
    for sql in sqls:
        #print sql
        g1= query_db(c,sql)
        for k in g1: 
            for e in k:
                print ('%s'%e).encode('utf8'),
            print '\t'

if __name__=='__main__':
    main()
