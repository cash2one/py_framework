#!/usr/bin/python
#!coding:utf8
import sys

dim_t='''
1,platform
2,pvarea
3,mall_src
4,mall_src_type
5,province
6,city
'''
tp_sh='''#!/bin/sh
#@input=o_p04_web_mall_pv_init_i,o_p04_web_dlr_pv_init_i,dim.dim_comm_pvareaid
#@output=ads_1111_ec_page_flw_{0}
# Author: hanshu                         #
# Date: 2016-09-21                          #
# Describe:ads_1111_ec_page_flw_{0}             #
##装载config文件
. /data/sysdir/warehouse/config/hive_config.conf

run_date $1

hour=$(date +%H)
if [ $hour -gt 12 ]
then
  etl_date=$(date +%F)
fi
etl_date=${{1:-$etl_date}}

echo $etl_date

cd $hbase_bin_path
hive -hivevar dt=$etl_date -f $scriptpath/ads/ads_1111/hql/ads_1111_ec_page_flw_{0}.hql
'''

tp_v1_hql='''
select 
    report_time_{0} as report_time,page_type,object_id,object_name,
    '{1}' as dimension_type,{2}_id as dimension_value,{2}_name as dimension_name,
    count(*) pv, count(distinct uid) uv 
from base_t
group by  report_time_{0},page_type,object_id,object_name,{2}_id,{2}_name
'''

tp_create='''
use ads;
drop table if exists ads.ads_1111_ec_page_flw_{0};
create external table ads.ads_1111_ec_page_flw_{0}
(
 report_time                   string  comment'报表日期'
,page_type                     string  comment'页面类型 (1：专题页,2：主会场,3：A-金融分会场,4：B-品牌分会场,5：经销商分会场,6：异业合作分会场,7：9.9拍红包,8：1元秒杀红包)'
,object_id                     string  comment'对象id  (页面类型为4时，为品牌id，页面类型为7和8时为红包商品Id)'
,object_name                   string  comment'对象名称 (页面类型是4时是品牌名称，页面类型是7和8时是红包商品名称)'
,dimension_type                string  comment'维度类型 (1：终端,2：pvareaid,3：mall来源,4：mall来源类型,5：省份,6：城市)'
,dimension_value               string  comment'维度值'
,dimension_name                string  comment'维度值名称'
,pv                            string  comment'Pv'
,uv                            string  comment'Uv'
)
comment '双11购车节每 {1} 流量'
PARTITIONED BY (dt STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\007' LINES TERMINATED BY '\\n'
STORED AS RCFILE
LOCATION  '/warehouse/ads/ads_1111/ads_1111_ec_page_flw_{0}';
'''


tp_hql='''
select 
    report_time_{0} as report_time,
    page_type,object_id,object_name,
    case
        {4}
        else '-9'
    end as dimension_type,
    coalesce({1},'-9') 
        as dimension_value,
    coalesce({2},'汇总') 
        as dimension_name,
    count(*) pv, 
    count(distinct uid) uv 
from base_t
group by  report_time_{0},page_type,object_id,object_name,
        {1},
        {2}
grouping sets ({3})
'''
tp_hql_suffix='''--###############################################################################
-- 功能描述：页面{0}流量监控
-- 按分钟计算 明细维度下 pv,uv量
-- 输入：
--       ods.o_p04_web_mall_pv_init_i,  dim.dim_comm_pvareaid,  dim.dim_city
-- 输入视图: ads.ads_1111_ec_page_flw_view
-- 输出: ads.ads_1111_ec_page_flw_{0}
-- 参数：
--       ${{hivevar:dt}}  执行日期，格式 yyyy-mm-dd
--       ##${{hivevar:end_hour}}   累计统计终结小时，格式 12 或者 24
-- 创建人：hanshu
-- 创建时间：2016-09-22
--###############################################################################
set hive.exec.compress.output=true;
set mapred.output.compress=true;
set mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec;
set hive.exec.parallel=true;
set hive.auto.convert.join=false;
set hive.map.aggr=true;

with base_t as ( select * from ads.ads_1111_ec_page_flw_view where dt='${{hivevar:dt}}')

insert overwrite table ads.ads_1111_ec_page_flw_{0} partition(dt='${{hivevar:dt}}')    
'''

rarr=[]

def apply_tp_v1_hql(time_interval):
    for l in dim_t.strip().split('\n'):
        arr=l.strip().split(',')
        if len(arr)<2:continue
        this_str= tp_v1_hql.format(time_interval,arr[0],arr[1])
        rarr.append(this_str)
    print tp_hql_suffix
    print '\n  union all\n'.join(rarr)
    print ';'

def apply_tp_hql(time_interval):    
    rarr=[]
    ret_st=''
    for l in dim_t.strip().split('\n'):
        arr=l.strip().split(',')
        if len(arr)<2:continue
        rarr.append(arr[1])
    
    dim_value_st=','.join(['%s_id'%field for field in rarr])
    dim_name_st=','.join(['%s_name'%field for field in rarr])
    
    grouping_sets_st='   ,'.join([
        '(report_time_%s,page_type,object_id,object_name,%s_id,%s_name)\n'%
        (time_interval,field,field) for field in rarr
     ])
    # extra sum grouping 
    grouping_sets_st+='   ,(report_time_%s,page_type,object_id,object_name)'%time_interval
    
    case_when_st='        '.join(['when %s_id is not null then \'%d\' \n'%(field,i+1) for i,field in enumerate(rarr)])
    ret_st+=tp_hql_suffix.format(time_interval)+'\n'
    ret_st+=tp_hql.format(time_interval,dim_value_st,dim_name_st,grouping_sets_st,case_when_st)+';\n'
    return ret_st
    
def get_output(fname):
    # return sys.stdout
    return open(fname,'wb')
    
    
def gen_sql_shell_create():
    import traceback,os
    global tp_sh,tp_create
    for sub in ('create_table','hql','sh'):
        try:os.mkdir(sub)
        except Exception,e:print 'mkdir error: ',e
    for time_interval in ('1_minute','10_minute','30_minute','hour'):
        st=apply_tp_hql(time_interval)
        fname='hql\\ads_1111_ec_page_flw_%s.hql'%time_interval
        out=get_output(fname)
        out.write(st)
        
        fname='sh\\ads_1111_ec_page_flw_%s.sh'%time_interval
        out=get_output(fname)
        ch_name=time_interval.replace('hour','小时').replace('_minute','分钟')
        print tp_sh
        out.write( tp_sh.format(time_interval,ch_name).strip() )
        
        continue
        
        fname='create_table\\create_ads_1111_ec_page_flw_%s.hql'%time_interval
        out=get_output(fname)
        ch_name=time_interval.replace('hour','小时').replace('_minute','分钟')
        out.write(tp_create.format(time_interval,ch_name) )
        
        
    
if __name__=='__main__':
    gen_sql_shell_create()
    # gen_rownum()