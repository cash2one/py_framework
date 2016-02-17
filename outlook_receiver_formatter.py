import re
class glb:
    pat = re.compile('.*<(.*)@.*')
def to_log_mail_address(st):
    a=s.split(';')
    d=[glb.pat.match(i).group(1) for i in a]
    print ','.join(d)
s='DENG,WEI <dengwei02@baidu.com>; Guo,Langbo <guolangbo@baidu.com>; Han,Shu <hanshu@baidu.com>; Jin,Baohua <jinbaohua@baidu.com>; Kang,Lijia <kanglijia@baidu.com>; Li,Zheng(OPPD) <lizheng08@baidu.com>; Wang,Yan(OPPD) <wangyan35@baidu.com>; Wu,Qiong(OPPD01) <wuqiong03@baidu.com>; Zhao,Zhixing <zhaozhixing@baidu.com>'
to_log_mail_address(s)