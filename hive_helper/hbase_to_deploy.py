import datetime,glob
import os,shutil,sys
conf={'hanshu':['']}
hanshu='''
ads_1111_ec_page_flw_1_minute
ads_1111_ec_page_flw_10_minute
ads_1111_ec_page_flw_30_minute
ads_1111_ec_page_flw_hour
# ads_1111_ec_page_accu_flw_day
ads_1111_ec_page_accu_flw_hour
'''.strip().split('\n')
create_temp='''create '{0}',{{ NAME => 'cf' ,VERSIONS => 1 , COMPRESSION => 'GZ' }},  {{NUMREGIONS => 2, SPLITALGO => 'HexStringSplit'}}
'''
dirs=('hql','create_table','sh')
conf['hanshu']=hanshu

def get_output(fname):
    return sys.stdout
    # return open(fname,'wb')

date= datetime.datetime.now().strftime('%Y%m%d')
user='hanshu'
dirname='_'.join(['dw',date,user])
try:os.mkdir(dirname)
except:pass

for tbname in conf[user]:
    out=get_output(tbname+".hbase.hql")
    # hql=create_temp.format(tbname)
    # out.write('echo "%s"|hbase shell'%hql)
    hql='else if ("{0}".equals(tablename)){{\n}}'.format(tbname)
    out.write('%s'%hql)
    out.write('\n')