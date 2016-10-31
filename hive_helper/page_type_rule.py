#:coding:gbk
pt_st='''
1  专题页/主会场规则：site_id为58，1211058，category_id 为583，sub_category_id为5031，object_id 为3333。
4  品牌分会场：site_id为58，1211058，category_id 为583，sub_category_id为5031，object_id 为品牌Id（品牌待定）。
3  金融分会场：site_id为58，1211058，category_id 为583，sub_category_id为5031，object_id 为3420
6  异业合作分会场：site_id为58，1211058，category_id 为583，sub_category_id为5031，object_id 为3418
8  1元秒杀详情页：site_id为58，1211058，category_id 为582，sub_category_id为3338，object_id为商品Id，与stage.s_m05_item关联，取source=16的，再与stage.s_m05_item_config关联取event_id=128的
7  9.9元拍红包详情页：site_id为58，1211058，category_id 为582，sub_category_id为3338，object_id为商品Id，与stage.s_m05_item关联，取source=15的，再与stage.s_m05_item_config关联取event_id=128的
'''
doc_st='''
1：专题页
2：主会场
3：A-金融分会场
4：B-品牌分会场
5：经销商分会场
6：异业合作分会场
7：9.9拍红包
8：1元秒杀红包
'''
print pt_st
case_s='''
        case when  ( aa.site_id in ('58','1211058') and aa.category_id ='583' and aa.sub_category_id ='5031' )
            then
                case 
                    when aa.object_id='3333' then '1'  --1：专题页/2：主会场
                    when aa.object_id='3420' then '3'  --3：A-金融分会场
                    when aa.object_id='3418' then '6'  --6：异业合作分会场
                    when aa.object_id='3440' then '4'  --4：B-品牌分会场                         
                    --dealer_id 关联 stage.s_m02_dso_provider provider_id区分不同品牌分会场
                    else null
                end
            when  ( aa.site_id in ('58','1211058') and aa.category_id ='582' and aa.sub_category_id ='3338' )
            then
                case --need connect new table !!!
                    when 1=1 then '7' --7：9.9拍红包 
                    -- 9.9元拍红包详情页：site_id为58，1211058，category_id 为582，sub_category_id为3338，
                    -- object_id为商品Id，与stage.s_m05_item关联，取source=15的，
                    -- 再与stage.s_m05_item_config关联取event_id=126的
                    when 1=1 then '8'  --8：1元秒杀红包 object_id为商品Id，与stage.s_m05_item关联，
                    -- 取source=16的，再与stage.s_m05_item_config关联取event_id=126的
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
    
    


