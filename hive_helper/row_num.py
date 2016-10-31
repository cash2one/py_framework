dim_t='''
1,platform
2,pvarea
3,mall_src
4,mall_src_type
5,province
6,city
'''

case_when_rn_st='''
when {0}_id is not null then 
    count( case when uv_row_num_{1}=1 then 1 else null  end )
'''     
rownum_temp='''
        row_number() over ( 
                partition by uid,{0} 
                order by report_time_1_minute asc
            ) as uv_row_num_{1},
'''   
def gen_rownum():
    rarr=[]
    for l in dim_t.strip().split('\n'):
        arr=l.strip().split(',')
        if len(arr)<2:continue
        rarr.append(arr[1])
    
    dim_value_st=','.join(['%s_id'%field for field in rarr])
    grouping_sets_st=[
        'uid,page_type,object_id,object_name,%s_id,%s_name'%
        (field,field) for field in rarr
     ]
    print dim_value_st
    for st in  grouping_sets_st:
        print rownum_temp.strip('\n').format(st,st.split(',')[-1].replace('_name',''))
    print ''
    print ''
    for st in  rarr:
        print case_when_rn_st.strip('\n').format(st,st)
        
gen_rownum()