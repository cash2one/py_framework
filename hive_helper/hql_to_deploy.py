import datetime,glob
import os,shutil
conf={'hanshu':['']}
hanshu='''
ads_1111_ec_page_flw_1_minute
ads_1111_ec_page_flw_10_minute
ads_1111_ec_page_flw_30_minute
ads_1111_ec_page_flw_hour
ads_1111_ec_page_flw_day
ads_1111_ec_page_accu_flw_day
ads_1111_ec_page_accu_flw_hour
ads_1111_ec_finance_detail_page_flw_day
ads_1111_ec_brand_session_flw_day
ads_1111_ec_pratt_red_click_day
ads_1111_ec_red_recommend_guide_flw_day
ads_1111_ec_red_banner_guide_flw_day
ads_1111_ec_main_page_guide_flw_day
ads_1111_ec_detail_page_flw_day
##
ads_1111_ec_red_rain_click_day
######ads_1111_ec_fortune_red_click_day
ads_1111_ec_promotion_guide_flw_day
ads_1111_ec_item_detail_page_flw_day
'''.strip().split('\n')
on='''
ads_1111_ec_page_flw_hour
ads_1111_ec_page_accu_flw_day
ads_1111_ec_page_flw_30_minute
ads_1111_ec_page_flw_1_minute
ads_1111_ec_page_accu_flw_hour
ads_1111_ec_page_flw_10_minute
ads_1111_ec_qr_code_scan_day
ads_1111_ec_finance_detail_page_flw_day
ads_1111_ec_red_banner_guide_flw_day
ads_1111_ec_page_flw_day
ads_1111_dlr_tgh_gch_order_info
ads_1111_ec_topic_leads_day
ads_1111_ec_app_flw_day
ads_1111_ec_qr_code_download_day
ads_1111_ec_cookie_subdomain_pvareaid
ads_1111_ec_main_page_guide_flw_day
ads_1111_ec_pratt_red_click_day
ads_1111_sem_monitor_day
ads_1111_ec_interaction_activity_day
ads_1111_ec_cookie_outside_pvareaid
ads_1111_dlr_tgh_activity_flw_dtl
ads_1111_ec_app_client_day
ads_1111_ec_brand_session_flw_day
ads_1111_sem_order_detail_day
ads_1111_ec_red_recommend_guide_flw_day
ads_1111_dlr_tgh_gch_city_flw_order_accu
ads_1111_dlr_tgh_gch_resource_flw_order_day
ads_1111_dlr_tgh_gch_city_flw_order_day
ads_1111_dlr_tgh_gch_resource_flw_order_accu
ads_1111_ec_red_rain_click_day
'''.strip().split('\n')
print set(hanshu)-set(on)
print set(on)-set(hanshu)
print len(set(on)) ,len(set(hanshu))
# exit()
dirs=('hql','create_table','sh')
conf['hanshu']=set(hanshu)-set(on)


date= datetime.datetime.now().strftime('%Y%m%d')
user='hanshu'
dirname='_'.join(['dw',date,user])
print conf[user]
# exit()
try:os.mkdir(dirname)
except:pass
for subdir in dirs:
    try:os.mkdir(dirname+'\\'+subdir)
    except:pass
    for fpart in conf[user]:
        if len(fpart)==0:continue
        for file in glob.glob('..\\%s\\*%s.*'%(subdir,fpart)):
            print file
            shutil.copy( file,'%s\\%s\\'%(dirname,subdir))
            