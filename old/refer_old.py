import re
from urllib import *
from urlparse import urlparse,parse_qs

def get_url_info(url):
    url_list = dict()
    url_list['url'] = url
    url_list['domain'] = '-'
    if url.find(".html") < 0 and url.find(".htm") < 0 and url.find(".shtml") < 0:
    ### 20141128 find bugs with if url[len(url)-1] != '/':string index out of range
        if len(url) > 1:
            if url[len(url)-1] != '/':
                url_list['url'] = url + "/"
    match = re.match('http://(.*)',url_list['url'])
    if match is not None:
        tmp_list = match.group(1).split("/")
        url_list['domain'] = tmp_list[0]
    return url_list

WISE_RULES = [
 [r'(?:http|https)\://(?:m|wap|md5|m5)\.baidu\.com/.*?word=(.*)',    'baidu',  'wise'],
 [r'(?:http|https)\://(?:www|m5)\.baidu\.com/.*from=.*?/.*?word=(.*)',  'baidu', 'wise'],
 [r'http\://m\.(?:haosou|so)\.com/[^?]*\?.*?q=(.*)','digit','wise'],
 [r'http\://(?:m|wap)\.sogou\.com/[^?]*\?.*?(?:key|keyword)=(.*)','sogou','wise'],
 [r'http\://(?:m|wap)\.soso\.com/[^?]*\?.*?key=(.*)','sogou','wise'],
 [r'(?:http|https)\://www\.google\.com/[^?]*\?.*?(?:query|q)=(.*)','google','wise'],
 [r'http\://cn\.bing\.com/[^?]*\?.*?q=(.*)','bing','wise'],
 [r'http\://(?:i|wap)\.easou\.com/[^?]*\?.*?q=(.*)','easou','wise'],
 [r'http\://m\.(?:(?:sa|yz|sj|sp)\.|)sm\.cn/[^?]*\?.*?q=(.*)','sm','wise']
] 
for row in WISE_RULES: row[0] = re.compile(row[0])
# print RULES

def get_refer_info_wise(url):
    url = unquote(url)
    regpat = rule[0]
    name = rule[1]
    type = rule[2]
    for rule in WISE_RULES:
        m = regpat.match(url):
        if m is not None:
            keyword = m.group(1)
            return name, keyword ,type
    return 'other','',type
    
def many_startswith(st,lst):
    for prefix in lst:
        if st.startswith(prefix):
            return True
    return False
    
def get_refer_info_old(refer):
    ret_list = dict()
    ret_list['refer'] = refer
    ret_list['target'] = 'other'
    ret_list['word'] = '-'
    ret_list['tn'] = '-'
    ret_list['query'] = '-'
    param_list = dict()
    if refer.find('http://www.baidu.com/ssid=') == 0 or refer.find('http://www.baidu.com/from=') == 0:
        return ret_list
    elif refer.find('http://www.baidu.com/') == 0 or  refer.find('https://www.baidu.com/') == 0:
        if refer.find('?') > 0:
            tmp = refer[refer.find('?')+1:]
            tmp_list = tmp.split("&")
            for k_v in tmp_list:
                k_v_tmp = k_v.split('=')
                if len(k_v_tmp) < 2:
                    break
                param_list[k_v_tmp[0]] = k_v_tmp[1]
                if k_v_tmp[0] == '':
                    break
                m = re.match(r'(?:wd|word|q1|w)=(.*)', k_v)
                if m is not None:
                    ret_list['word'] = m.group(1)
                    ret_list['target'] = 'baidu'
            if param_list.has_key("tn"):
                ret_list['tn'] = param_list['tn']
            else:
                if refer.find('tn=') < 0:
                    ret_list['refer'] = refer + "&tn=baidu"
                ret_list['tn'] = 'baidu'
    elif refer.find('http://www.so.com/') == 0 or refer.find('http://so.360.cn/') == 0 or refer.find('http://www.haosou.com/') == 0:
        if refer.find('?') > 0:
            tmp = refer[refer.find('?')+1:]
            tmp_list = tmp.split("&")
            for k_v in tmp_list:
                k_v_tmp = k_v.split('=')
                if len(k_v_tmp) < 2:
                    break
                param_list[k_v_tmp[0]] = k_v_tmp[1]
                if k_v_tmp[0] == '':
                    break
                m = re.match(r'q=(.*)', k_v)
                if m is not None:
                    ret_list['word'] = m.group(1)
                    ret_list['target'] = 'digit'
            if param_list.has_key("src"):
                ret_list['tn'] = param_list['src']
            else:
                ret_list['tn'] = 'digit'
    elif refer.find('http://www.soso.com/') == 0:
        if refer.find('?') > 0:
            tmp = refer[refer.find('?')+1:]
            tmp_list = tmp.split("&")
            for k_v in tmp_list:
                k_v_tmp = k_v.split('=')
                if len(k_v_tmp) < 2:
                    break
                param_list[k_v_tmp[0]] = k_v_tmp[1]
                if k_v_tmp[0] == '':
                    break
                #w has large amount of cheating flow
                m = re.match(r'query=(.*)', k_v)
                if m is not None:
                    ret_list['word'] = m.group(1)
                    ret_list['target'] = 'soso'
            if param_list.has_key("pid"):
                ret_list['tn'] = param_list['pid']
            else:
                ret_list['tn'] = 'soso'
    elif refer.find('http://www.sogou.com/') == 0:
        if refer.find('?') > 0:
            tmp = refer[refer.find('?')+1:]
            tmp_list = tmp.split("&")
            for k_v in tmp_list:
                k_v_tmp = k_v.split('=')
                if len(k_v_tmp) < 2:
                    break
                param_list[k_v_tmp[0]] = k_v_tmp[1]
                if k_v_tmp[0] == '':
                    break
                m = re.match(r'query=(.*)', k_v)
                if m is not None:
                    ret_list['word'] = m.group(1)
                    ret_list['target'] = "sogou"
            if param_list.has_key("pid"):
                ret_list['tn'] = param_list['pid']
            else:
                ret_list['tn'] = 'sogou'
    elif refer.find('http://www.google.com') == 0:
        if refer.find('?') > 0:
            tmp = refer[refer.find('?')+1:]
            tmp_list = tmp.split("&")
            for k_v in tmp_list:
                k_v_tmp = k_v.split('=')
                if len(k_v_tmp) < 2:
                    break
                param_list[k_v_tmp[0]] = k_v_tmp[1]
                if k_v_tmp[0] == '':
                    break
                m = re.match(r'(?:query|q)=(.*)', k_v)
                if m is not None:
                    ret_list['word'] = m.group(1)
                    ret_list['target'] = 'google'
    if ret_list['target'] != 'other':
        word = " ".join(ret_list['word'].split("+"))
        word = "".join(word.split("%00"))
        temp = unquote(word)
        query = '-'
        if param_list.has_key('ie'):
            try:
                query = temp.decode(param_list['ie']).encode('gb18030')
            except:
                query = temp
        else:
            try:
                query = temp.decode('utf-8').encode('gb18030')
            except:
                query = temp
        ret_list['query'] = query
    return ret_list