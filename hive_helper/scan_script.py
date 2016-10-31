import re
PAT=re.compile('aa\.(\w+)')

def get_identifier():
    set_f=set()
    fname='create_ads_1111_ec_page_flw_filter_view.hql'
    fname='create_ads_1111_ec_page_flw_view.hql'
    for l in open(fname):
        ms=PAT.findall(l)
        if len(ms)==0:continue
        for m in ms:
            print m
            set_f.add(m)
    print ','.join(sorted(set_f))

import sqlparse
import glob
def u2g(st):
    return st.encode('gbk','ignore')
    
def find_depend():
    for fname in glob.glob('../create_view/*.hql')+ glob.glob('../hql/*.hql'):
        st=''.join([l for l in open(fname).readlines()])
        sql= sqlparse.format( st,reindent=True)
        # print u2g(sql)
        print '[%s]'%fname
        for stat in sqlparse.parse(sql):
            for tk in recur_get(stat,0):
                print u2g(unicode(tk))
                    
def recur_get(stat,i):
    i=i+1
    for tok in  stat.tokens:
        if type(tok)==sqlparse.sql.Identifier:
            yield tok
        elif type(tok)==sqlparse.sql.Parenthesis:
            for tk in recur_get(tok,i):
                yield tk
        else:
            # print type(tok),u2g(unicode(tok))
            pass
    
find_depend()