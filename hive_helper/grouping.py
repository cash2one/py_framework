#!coding:gbk
s='''--ҳ������
page_type

--ҳ�����ͣ��ն�
page_type,platform
page_type,platform,app_soft_type
page_type,platform,app_soft_type,app_sys_type

--ҳ�����ͣ�pvid
page_type,pvarea_id

--ҳ�����ͣ�mall��Դ
page_type,subdomain_pvarea_id,subdomain_pvarea_id_type

--ҳ�����ͣ�mall��Դ����
page_type,subdomain_pvarea_id_type

--ҳ�����ͣ�ʡ��
page_type,province_id

--ҳ�����ͣ�����
page_type,province_id,city_id

--ҳ�����ͣ��նˣ�pvid
page_type,platform,pvarea_id
page_type,platform,app_soft_type,pvarea_id
page_type,platform,app_soft_type,app_sys_type,pvarea_id


--ҳ�����ͣ��նˣ�mall��Դ
page_type,platform,subdomain_pvarea_id,subdomain_pvarea_id_type
page_type,platform,app_soft_type,subdomain_pvarea_id,subdomain_pvarea_id_type
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id,subdomain_pvarea_id_type


--ҳ�����ͣ��նˣ�mall��Դ����
page_type,platform,subdomain_pvarea_id_type
page_type,platform,app_soft_type,subdomain_pvarea_id_type
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id_type


--ҳ�����ͣ��նˣ�ʡ��
page_type,platform,province_id
page_type,platform,app_soft_type,province_id
page_type,platform,app_soft_type,app_sys_type,province_id


--ҳ�����ͣ��նˣ�����
page_type,platform,province_id,city_id
page_type,platform,app_soft_type,province_id,city_id
page_type,platform,app_soft_type,app_sys_type,province_id,city_id


--ҳ�����ͣ�pvid��ʡ��
page_type,pvarea_id,province_id

--ҳ�����ͣ�pvid������
page_type,pvarea_id,province_id,city_id

--ҳ�����ͣ�mall��Դ��ʡ��
page_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id

--ҳ�����ͣ�mall��Դ������
page_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id

--ҳ�����ͣ�mall��Դ���ͣ�ʡ��
page_type,subdomain_pvarea_id_type,province_id

--ҳ�����ͣ�mall��Դ���ͣ�����
page_type,subdomain_pvarea_id_type,province_id,city_id


--ҳ�����ͣ��նˣ�pvid��ʡ��
page_type,platform,pvarea_id,province_id
page_type,platform,app_soft_type,pvarea_id,province_id
page_type,platform,app_soft_type,app_sys_type,pvarea_id,province_id


--ҳ�����ͣ��նˣ�pvid������
page_type,platform,pvarea_id,province_id,city_id
page_type,platform,app_soft_type,pvarea_id,province_id,city_id
page_type,platform,app_soft_type,app_sys_type,pvarea_id,province_id,city_id


--ҳ�����ͣ��նˣ�mall��Դ��ʡ��
page_type,platform,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id


--ҳ�����ͣ��նˣ�mall��Դ������
page_type,platform,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id
page_type,platform,app_soft_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id,subdomain_pvarea_id_type,province_id,city_id


--ҳ�����ͣ��նˣ�mall��Դ���ͣ�ʡ��
page_type,platform,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,subdomain_pvarea_id_type,province_id
page_type,platform,app_soft_type,app_sys_type,subdomain_pvarea_id_type,province_id

--ҳ�����ͣ��նˣ�mall��Դ���ͣ�����
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