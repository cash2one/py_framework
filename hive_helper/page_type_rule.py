#:coding:gbk
pt_st='''
1  ר��ҳ/���᳡����site_idΪ58��1211058��category_id Ϊ583��sub_category_idΪ5031��object_id Ϊ3333��
4  Ʒ�Ʒֻ᳡��site_idΪ58��1211058��category_id Ϊ583��sub_category_idΪ5031��object_id ΪƷ��Id��Ʒ�ƴ�������
3  ���ڷֻ᳡��site_idΪ58��1211058��category_id Ϊ583��sub_category_idΪ5031��object_id Ϊ3420
6  ��ҵ�����ֻ᳡��site_idΪ58��1211058��category_id Ϊ583��sub_category_idΪ5031��object_id Ϊ3418
8  1Ԫ��ɱ����ҳ��site_idΪ58��1211058��category_id Ϊ582��sub_category_idΪ3338��object_idΪ��ƷId����stage.s_m05_item������ȡsource=16�ģ�����stage.s_m05_item_config����ȡevent_id=128��
7  9.9Ԫ�ĺ������ҳ��site_idΪ58��1211058��category_id Ϊ582��sub_category_idΪ3338��object_idΪ��ƷId����stage.s_m05_item������ȡsource=15�ģ�����stage.s_m05_item_config����ȡevent_id=128��
'''
doc_st='''
1��ר��ҳ
2�����᳡
3��A-���ڷֻ᳡
4��B-Ʒ�Ʒֻ᳡
5�������̷ֻ᳡
6����ҵ�����ֻ᳡
7��9.9�ĺ��
8��1Ԫ��ɱ���
'''
print pt_st
case_s='''
        case when  ( aa.site_id in ('58','1211058') and aa.category_id ='583' and aa.sub_category_id ='5031' )
            then
                case 
                    when aa.object_id='3333' then '1'  --1��ר��ҳ/2�����᳡
                    when aa.object_id='3420' then '3'  --3��A-���ڷֻ᳡
                    when aa.object_id='3418' then '6'  --6����ҵ�����ֻ᳡
                    when aa.object_id='3440' then '4'  --4��B-Ʒ�Ʒֻ᳡                         
                    --dealer_id ���� stage.s_m02_dso_provider provider_id���ֲ�ͬƷ�Ʒֻ᳡
                    else null
                end
            when  ( aa.site_id in ('58','1211058') and aa.category_id ='582' and aa.sub_category_id ='3338' )
            then
                case --need connect new table !!!
                    when 1=1 then '7' --7��9.9�ĺ�� 
                    -- 9.9Ԫ�ĺ������ҳ��site_idΪ58��1211058��category_id Ϊ582��sub_category_idΪ3338��
                    -- object_idΪ��ƷId����stage.s_m05_item������ȡsource=15�ģ�
                    -- ����stage.s_m05_item_config����ȡevent_id=126��
                    when 1=1 then '8'  --8��1Ԫ��ɱ��� object_idΪ��ƷId����stage.s_m05_item������
                    -- ȡsource=16�ģ�����stage.s_m05_item_config����ȡevent_id=126��
                    else null                                
                end
            else null
        end as page_type,
'''

join_s='''
    from ods.o_p04_web_mall_pv_init_i  aa
    left outer join stage.s_m02_dso_provider bb
        on a.dealer_id=b.dealerid
    left outer join stage.s_m05_item cc
        on 1=2
    left outer join stage.s_m05_item_config  dd
        on 1=2
'''


import glob,os
for fn in glob.glob('../create_view/*.hql'):
    flg=True
    for l in open(fn):
        if flg:
            print l.strip('\n')
        if l.find('__start')!=-1:
            print case_s
            flg=False
        if l.find('__end')!=-1:
            print l.strip('\n')
            flg=True
    
    


