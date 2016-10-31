#!coding:gbk
s='''--页面类型
page_type

--页面类型，终端
page_type,platform
page_type,platform,app_soft_type
page_type,platform,app_soft_type,app_sys_type

--页面类型，pvid
page_type,pvarea_id

--页面类型，mall来源
page_type,subdomain_pvarea_id,subdomain_pvarea_id_type

--页面类型，mall来源类型
page_type,subdomain_pvarea_id_type

--页面类型，省份
page_type,province_id

--页面类型，城市
page_type,province_id,city_id

--页面类型，终端，pvid
page_type,platform,pvarea_id
page_type,platform,app_soft_type,pvarea_id
page_type,platform,app_soft_type,app_sys_type,pvarea_id


--页面类型，终端，mall来源
page_type,platform,subdomain_pvarea_id,subdomain_pvarea_id_type
page_type,platform,app_soft_type,subdomain_pvarea_id,subdomain_pvarea_id_type
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id,subdomain_pvarea_id_type


--页面类型，终端，mall来源类型
page_type,platform,subdomain_pvarea_id_type
page_type,platform,app_soft_type,subdomain_pvarea_id_type
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id_type


--页面类型，终端，省份
page_type,platform,province_id
page_type,platform,app_soft_type,province_id
page_type,platform,app_soft_type,app_sys_type,province_id


--页面类型，终端，城市
page_type,platform,province_id,city_id
page_type,platform,app_soft_type,province_id,city_id
page_type,platform,app_soft_type,app_sys_type,province_id,city_id


--页面类型，pvid，省份
page_type,pvarea_id,province_id

--页面类型，pvid，城市
page_type,pvarea_id,province_id,city_id

--页面类型，mall来源，省份
page_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id

--页面类型，mall来源，城市
page_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id

--页面类型，mall来源类型，省份
page_type,subdomain_pvarea_id_type,province_id

--页面类型，mall来源类型，城市
page_type,subdomain_pvarea_id_type,province_id,city_id


--页面类型，终端，pvid，省份
page_type,platform,pvarea_id,province_id
page_type,platform,app_soft_type,pvarea_id,province_id
page_type,platform,app_soft_type,app_sys_type,pvarea_id,province_id


--页面类型，终端，pvid，城市
page_type,platform,pvarea_id,province_id,city_id
page_type,platform,app_soft_type,pvarea_id,province_id,city_id
page_type,platform,app_soft_type,app_sys_type,pvarea_id,province_id,city_id


--页面类型，终端，mall来源，省份
page_type,platform,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id


--页面类型，终端，mall来源，城市
page_type,platform,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id
page_type,platform,app_soft_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id


--页面类型，终端，mall来源类型，省份
page_type,platform,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id_type,province_id

--页面类型，终端，mall来源类型，城市
page_type,platform,subdomain_pvarea_id_type,province_id,city_id
page_type,platform,app_soft_type,subdomain_pvarea_id_type,province_id,city_id
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id_type,province_id,city_id'''
def chain_replace(st):
    dic=['platform','app_soft_type','app_sys_type']
    for f_st in dic: st=st.replace(f_st,f_st+'_id')
    dic={'subdomain_pvarea_id_type':'subdomain_pvarea_id'}
    for f_st,t_st in dic.items(): st=st.replace(f_st,f_st+'_id')
    return st
    
for l in s.strip().split('\n'):
    if l.startswith('--'):
        print '   ',l
    elif len(l)==0:continue
    else:
        print '    (%s),'%chain_replace(l)