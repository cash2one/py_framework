#!coding:utf8
col_info='''
a.pvareaid
e.pvarea_desc as pvarea_name
d.province_id
d.province_name
a.bussiness_type
a.city_id
c.city_name
a.dealer_id
f.name as dealer_name
g.brand_id
g.brand_name
a.series_id
g.series_name
a.spec_id
h.spec_name
a.object_id as item_id
i.name as item_name'''
col_info2='''
    coalesce(platform,'-9'),
    coalesce(app_soft_type,'-9'),
    coalesce(app_sys_type,'-9'),
    coalesce(pvareaid,'-9') as pvareaid,
    coalesce(pvarea_name,'汇总') as pvarea_name,
    coalesce(city_id,'-9') as city_id,
    coalesce(city_name,'汇总') as city_name,
    coalesce(province_id,'-9') as province_id,
    coalesce(province_name,'汇总') as province_name,
    coalesce(dealer_id,'-9') as dealer_id,
    coalesce(dealer_name,'汇总') as dealer_name,
    coalesce(brand_id,'-9') as brand_id,
    coalesce(brand_name,'汇总') as brand_name,
    coalesce(series_id,'-9') as series_id,
    coalesce(series_name,'汇总') as series_name,
    coalesce(spec_id,'-9') as spec_id,
    coalesce(spec_name,'汇总') as spec_name,
    coalesce(item_id,'-9') as item_id,
    coalesce(item_name,'汇总') as item_name,
'''
col_info='''
b.event_num,
d.province_id,
d.province_name,
a.city_id,
c.city_name,
a.subdomain_pvarea_id,
e.pvarea_desc as pvarea_name,
f.pvarea_type_id,
f.pvarea_type_name,
'''
import re
PAT=re.compile('(\w+)?\.?(\w+)\s?(?:as)?\s?(\w+)?,?')
def parse_col_info(col_info,PAT):
    col_arr=[]
    for l in col_info.strip('\n').split('\n'):
        m=PAT.match(l)
        if not m:
            print 'not match:',l
            continue
        tb_alias,col_name,to_col_name= m.groups()
        if not to_col_name:
            to_col_name=col_name
        if col_name.endswith('id'):
            type='id'
        else:
            type='name'
        col_arr.append((tb_alias,col_name,to_col_name,type))
    return col_arr

def u2g(st):
    return st.decode('utf8').encode('gbk')
    
def get_fill_null_col_str(col_arr):
    st=''
    for row in col_arr:
        tb_alias,col_name,to_col_name,type=row
        if type=='id':
            fill='-1'
        if type=='name':
            fill='其他'
        st+="coalesce({2}.{0},'{3}') as {1},\n".format(col_name,to_col_name,tb_alias,fill)
    print 'fill null:\n',u2g(st)
    return

def get_sum_col_str(col_arr):
    st=''
    for row in col_arr:
        tb_alias,col_name,to_col_name,type=row
        if type=='id':
            fill='-9'
        if type=='name':
            fill='汇总'        
        st+="coalesce({0},'{1}') as {0},\n".format(to_col_name,fill)
    print 'sum up:\n',u2g(st)
    return
    
def get_plain_col_str(col_arr):
    st=''
    for row in col_arr:
        tb_alias,col_name,to_col_name,type=row
        st+="{0},\n".format(to_col_name)
    print 'plain:\n',u2g(st)
    return
    
if __name__=='__main__':
    print col_info
    col_arr=parse_col_info(col_info,PAT)
    # for col in col_arr: print col
    print ','.join([col[2] for col in col_arr])
    get_fill_null_col_str(col_arr)
    get_sum_col_str(col_arr)
    get_plain_col_str(col_arr)