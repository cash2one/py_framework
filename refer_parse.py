import re
from urllib import unquote
from urlparse import urlparse,parse_qsl

def startswith_any(st,lst):
    for prefix in lst:
        if st.startswith(prefix):
            return True
    return False
    
def get_any_param(qsobj,lst):
    # print qsobj
    for qs in qsobj:
        for pname in lst:
            if qs[0] == pname:
                return qs[1]
    return "-"
    
def kv_split(st,asep,ksep):
    rlst = []
    for pair in st.split(asep):
        arr =pair.split(ksep)
        key = arr[0]
        value = arr[1] if len(arr)>1 else ''
        rlst.append((key,value))
    return rlst
    
def get_any_param(url,lst):
    uarr = url.split('?')
    base = uarr [0]    
    qstr = uarr[1] if len(uarr)>1 else ''
    qlst = kv_split(qstr,'&','=')    
    for qtup in qlst:
        if qtup[0]  in lst:
            return qtup[1]    
    return '-'
    
def find_any(st,lst):
    for part in lst:
        if st.find(part)!=-1:
            return True
    return False
    
PS_RULES = [
#['search engine name',['hostname'],['query_para_name'],['tn_para_name']],
  [
    'baidu', ## se name 
    ['www.baidu.com'], ## se domain
    ['wd','word','q1','w'], ## se query parameter name
    ['tn'] ## se source parameter name
  ],
  [
    'digit',
    ['www.so.com','so.360.cn','www.haosou.com'],
    ['q'],
    ['src']
  ],
  [
    'soso',
    ['www.soso.com'],
    ['query'],
    ['pid','p','sourceid','hdq']
  ],
  [
    'sogou',
    ['www.sogou.com'],
    ['query'],
    ['pid','p','sourceid','hdq']
  ],
  [
    'google',
    ['www.google.com'],
    ['query','q'],
    []
  ],
]
NOSEARCH_REFER=[
'http://www.baidu.com/ssid=',
'http://www.baidu.com/from=',
]
def get_refer_info_ps(refer):
    urlobj = urlparse(refer)
    qslst = parse_qsl(urlobj[4])
    site = 'other'
    word = '-'
    query = '-'
    tn = '-'
    if find_any(refer,NOSEARCH_REFER): 
        return site,query,tn,new_refer
    for rule in PS_RULES:
        if startswith_any( urlobj[1] ,rule[1]):
            site = rule[0]
            word = get_any_param(refer,rule[2])
            tn = get_any_param(refer,rule[3])
            if tn == '-' :
                tn = site
            new_refer = refer
            if site=='baidu' and refer.find('tn=') < 0:
                new_refer = refer + "&tn=baidu"
    if site != 'other':
        word = " ".join( word.split("+") )
        word = "".join( word.split("%00") )
        unq_s = unquote(word)
        encod = 'utf-8'
        for qs in qslst:
            if qs[0] == 'ie':
                encod = qs[1]
        try:
            query = unq_s.decode(encod).encode('gb81030')
        except:
            query = unq_s
    return site,word,query,tn,new_refer

WISE_RULES = [
 [r'(?:http|https)\://(?:m|wap|md5|m5)\.baidu\.com/.*?word=([^&]*)',    'baidu',  'wise'],
 [r'(?:http|https)\://(?:www|m5)\.baidu\.com/.*from=.*?/.*?word=([^&]*)',  'baidu', 'wise'],
 [r'http\://m\.(?:haosou|so)\.com/[^?]*\?.*?q=([^&]*)','digit','wise'],
 [r'http\://(?:m|wap)\.sogou\.com/[^?]*\?.*?(?:key|keyword)=([^&]*)','sogou','wise'],
 [r'http\://(?:m|wap)\.soso\.com/[^?]*\?.*?key=([^&]*)','sogou','wise'],
 [r'(?:http|https)\://www\.google\.com/[^?]*\?.*?(?:query|q)=([^&]*)','google','wise'],
 [r'http\://cn\.bing\.com/[^?]*\?.*?q=([^&]*)','bing','wise'],
 [r'http\://(?:i|wap)\.easou\.com/[^?]*\?.*?q=([^&]*)','easou','wise'],
 [r'http\://m\.(?:(?:sa|yz|sj|sp)\.|)sm\.cn/[^?]*\?.*?q=([^&]*)','sm','wise']
] 
for row in WISE_RULES: row[0] = re.compile(row[0])
# print RULES

def get_refer_info_wise(url):
    url = unquote(url)    
    for rule in WISE_RULES:
        regpat = rule[0]
        name = rule[1]
        type = rule[2]
        m = regpat.match(url)
        if m is not None:
            keyword = m.group(1)
            return name, keyword ,type
    return 'other','-',type
    
    
def main():
    url='http://www.sogou.com/tx?query=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98&hdq=sogou-site-c91e3483cf4f9005-1002&ekv=1&sourceid=sugg&ie=utf8&#nmb'
    print get_refer_info_ps(url)
    print get_refer_info_wise(url)
    
if __name__ == '__main__':
    main()