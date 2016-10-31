#coding:utf8
import re
import datetime
#####################################################
create_full_tp='''
use ads;
drop table if exists ads.{0};
create external table ads.{0}
(
{1}
)
comment '{2}'
PARTITIONED BY (dt STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\007' LINES TERMINATED BY '\\n'
STORED AS RCFILE
LOCATION  '/warehouse/ads/ads_1111/{0}';
'''
hql_tp='''
--###############################################################################
-- {comment}
-- 输入：
--       {depend}        
-- 输出: ads.{tbname}
-- 参数：
--       ${{hivevar:dt}}  执行日期，格式 yyyy-mm-dd
-- 创建人：{user}
-- 创建时间：{date}
--###############################################################################
set hive.exec.compress.output=true;
set mapred.output.compress=true;
set mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec;
set hive.exec.parallel=true;
set hive.auto.convert.join=false;
set hive.map.aggr=true;
-- explain
insert overwrite table ads.{tbname} partition(dt='${{hivevar:dt}}') 
'''
shell_tp='''
#!/bin/sh
#@input={depend}
#@output={tbname}
# Author: {user}                         #
# Date: {date}                          #
# Describe:{tbname}              #
##装载config文件
. /data/sysdir/warehouse/config/hive_config.conf
run_date $1
echo $etl_date
hive -hivevar dt=$etl_date -f $scriptpath/ads/ads_1111/hql/{tbname}.hql
'''

tb_lst=[]

############################################
tbcomment='普惠红包点击量-日（ads_1111_ec_pratt_red_click_day）'
dep='o_p04_web_mall_1111_hongbao_click_i'
col_info='''
report_date	时间	string	20160922
click_cnt	点击次数	string	
click_user_num	点击人数	string	Pc、m的取cuid，app的取device_id，取不到再取cuid
'''#dt	时间分区	string
# tb_lst.append((tbcomment,col_info,dep))

############################################
tbcomment='红包详情页推荐位导流-日（ads_1111_ec_red_recommend_guide_flw_day）'
dep='o_p04_web_mall_pv_init_filter_i,dim.dim_1111_ec_red_item_info'
col_info='''
report_date	时间	string	20160922
factory_id	厂商Id	string	Refer页的厂商 -9：汇总
factory_name	厂商名称	string	
series_id	车系Id	string	落地页的车系 -9：汇总
series_name	车系名称	string	
spec_id	车型Id	string	落地页的车型 -9：汇总
spec_name	车型名称	string	
item_id	商品Id	string	落地页的商品 -9：汇总
item_name	商品名称	string	
pv	Pv	string	
uv	Uv	string	
'''
# tb_lst.append((tbcomment,col_info,dep))


############################################
tbcomment='红包详情页通栏导流-日（ads_1111_ec_red_banner_guide_flw_day）'
dep='o_p04_web_mall_pv_init_filter_i,dim.dim_1111_ec_red_item_info'
col_info='''
report_date	时间	string	20160922
factory_id	厂商Id	string	指主会场的refer页的object_id对应的厂商
factory_name	厂商名称	string	
pv	Pv	string	
uv	Uv	string	
'''
# tb_lst.append((tbcomment,col_info,dep))

############################################
tbcomment='主会场向下导流-日（ads_1111_ec_main_page_guide_flw_day）'
dep='o_p04_web_mall_pv_init_filter_i,dim_comm_pvareaid,dim_city'
col_info='''
report_date	时间	string	20160922
platform	访端	string	01：pc  02：m  03：app -9：合计
app_soft_type	App软件类型	string	01：主软件  02：报价软件 03：车商城软件04：其他app -1：其他  -9：合计
app_sys_type	App系统类型	string	01：ios  02：android -1：其他 -9：合计
pvarea_id	Pvareaid	string	-9：合计
pvarea_id_name	Pvareaid名称	string	
province_id	省份Id	string	-9：合计
province_name	省份名称	string	
city_id	城市Id	string	-9：合计
city_name	城市名称	string	
pv	Pv	string	
uv	Uv	string	
'''
# tb_lst.append((tbcomment,col_info,dep))

############################################
tbcomment='详情页流量-日（ads_1111_ec_detail_page_flw_day）'
dep='o_p04_web_mall_pv_init_filter_i,stage.s_m02_dso_provider'
col_info='''
report_date	时间	string	20160922
platform	访端	string	01：pc  02：m  03：app -9：合计
app_soft_type	App软件类型	string	01：主软件  02：报价软件 03：车商城软件04：其他app -1：其他 -9：合计
app_sys_type	App系统类型	string	01：ios  02：android -1：其他 -9：合计
pvarea_id	Pvareaid	string	-9：合计
pvarea_id_name	Pvareaid名称	string	
province_id	省份Id	string	-9：合计
province_name	省份名称	string	
city_id	城市Id	string	-9：合计
city_name	城市名称	string	
business_type	业务类型	string	Page_custom_vars中的type值 -9：合计
dealer_id	商家Id	string	日志中的dealer_id -9：合计
dealer_name	商家名称	string	Dealer_id与stage.s_m02_dso_provider的provider_id关联，取name
brand_id	品牌Id	string	用车系id关联维表得到 -9：合计
brand_name	品牌名称	string	
series_id	车系Id	string	-9：合计
series_name	车系名称	string	
spec_id	车型Id	string	-9：合计
spec_name	车型名称	string	
item_id	商品Id	string	日志中的object_id -9：合计
item_name	商品名称	string	Object_id关联stage.s_m05_item取商品名称
pv	Pv	string	
uv	Uv	string	
'''
# tb_lst.append((tbcomment,col_info,dep))

############################################
tbcomment='红包雨点击-日（ads_1111_ec_red_rain_click_day）'
dep='o_p04_web_mall_1111_hongbao_count_i,o_p04_web_mall_pv_init_i,dim_comm_pvareaid,dim_city,dim_ec_pvarea_type'
col_info='''
report_date	时间	string	20160922
dimension_type	维度类型	string	1：场次 5：省份 6：城市 4：子站来源 5：子站来源类型
dimension_value	维度值	string	场次： 1：上午场 2：下午场 3：晚上场  按点击日志的时间划分，12：00前为上午场，12：00至18：00为下午场，其他为晚上场  子站来源类型： 1：站内 2：站外 0：其他 ……  不分维度时为-9
dimension_name	维度值名称	string	
click_user_num	点抢人数	string	
'''
# tb_lst.append((tbcomment,col_info,dep))

############################################
tbcomment='财神红包点击-日（ads_1111_ec_fortune_red_click_day）'
dep='o_p04_web_mall_1111_hongbao_count_i,o_p04_web_mall_pv_init_i,dim_comm_pvareaid,dim_city,dim_ec_pvarea_type'
col_info='''
report_date	时间	string	20160922
factory_id	厂商Id		点击日志的dealer_id
factory_name	厂商名称		点击日志的dealer_id与stage.s_m02_dso_provider的provider_id关联，取name
dimension_type	维度类型	string	1：场次 5：省份 6：城市 4：子站来源 5：子站来源类型
dimension_value	维度值	string	场次： 1：上午场 2：下午场 3：晚上场 按点击日志的时间划分，12：00前为上午场，12：00至18：00为下午场，其他为晚上场 子站来源类型： 1：站内 2：站外 0：其他 ……  不分维度时为-9
dimension_name	维度值名称	string	
click_user_num	点抢人数	string	
'''

# tb_lst.append((tbcomment,col_info,dep))

############################################
tbcomment='详情页促销位置导流-日（ads_1111_ec_promotion_guide_flw_day）'
dep='o_p04_web_mall_pv_init_filter_i,dim_series_view,dim_spec_view'
col_info='''
report_date	时间	string	20160922
brand_id	品牌Id	string	用车系id关联维表得到 -9：合计
brand_name	品牌名称	string	
series_id	车系Id	string	-9：合计
series_name	车系名称	string	
spec_id	车型Id	string	-9：合计
spec_name	车型名称	string	
item_id	商品Id	string	日志中的object_id -9：合计
pv	Pv	string	
uv	Uv	string	
'''

tb_lst.append((tbcomment,col_info,dep))

############################################
tbcomment='商品详情页流量-日（ads_1111_ec_item_detail_page_flw_day）'
dep='o_p04_web_mall_pv_init_filter_i,dim_series_view,dim_spec_view'
col_info='''
report_date	时间	string	20160922
brand_id	品牌Id	string	用车系id关联维表得到 -9：合计
brand_name	品牌名称	string	
series_id	车系Id	string	-9：合计
series_name	车系名称	string	
spec_id	车型Id	string	-9：合计
spec_name	车型名称	string	
item_id	商品Id	string	日志中的object_id -9：合计
pv	Pv	string	
uv	Uv	string	
'''

tb_lst.append((tbcomment,col_info,dep))

def u2g(st):
    return st.decode('utf8').encode('gbk')
    
P_tbname=re.compile('（(\w+)）')    
def apply_create(create_full_tp,tbcomment,col_info):
    tbname=P_tbname.findall(tbcomment)[0].strip()
    col_st=''
    for l in col_info.strip('\n').split('\n'):
        row= l.strip('\n').split('\t')
        if len(row)<4:print row;continue
        st= " ,{0}                   {2}  comment'{1} {3}'".format(row[0],row[1],row[2],row[3])
        col_st+=st+"\n"
    # col_st
    sql=create_full_tp.format(tbname,col_st.strip(' ,'),tbcomment)
    return tbname,sql
    
if __name__=='__main__':
    import os
    try:os.mkdir('output')
    except:pass
    dt= datetime.datetime.now().strftime('%Y-%m-%d')
    f_create=True
    f_hql=True
    # f_hql=False
    f_shell=True
    # f_shell=False
    for tbcomment,col_info,dep in tb_lst:
        
        tbname,sql=apply_create(create_full_tp,tbcomment,col_info)
        if f_create:
            with open('output/create_{}.hql'.format(tbname),'wb') as fh:
                print u2g(sql)
                fh.write(sql)
        
        hql=hql_tp.format(tbname=tbname,depend=dep,user='hanshu',date=dt,comment=tbcomment)
        hql=hql.strip('\n')
        if f_hql:
            with open('output/{}.hql'.format(tbname),'wb') as fh:
                print u2g(hql)
                fh.write(hql)
            
        shell=shell_tp.format(tbname=tbname,depend=dep,user='hanshu',date=dt,comment=tbcomment)
        shell=shell.strip('\n')
        if f_shell:
            with open('output/{}.sh'.format(tbname),'wb') as fh:
                print u2g(shell)
                fh.write(shell)