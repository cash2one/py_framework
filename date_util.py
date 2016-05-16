import time,datetime

FMT='%Y-%m-%d'

def str2date(str_date,fmt=FMT):    
    dobj = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str_date,fmt)))
    return dobj
    
def get_date(fmt=FMT,base= datetime.datetime.now(), isobj=False, **kwargs ):
    i_str2date=lambda str_date,fmt: datetime.datetime.fromtimestamp(time.mktime(time.strptime(str_date,fmt)))
    if type(base)==str:
        dateobj= i_str2date(base)+ datetime.timedelta( **kwargs)
    else:
        dateobj = base + datetime.timedelta( **kwargs)
    if isobj: 
        return dateobj
    else: 
        return dateobj.strftime(fmt)
        

    
def get_date_obj( base=datetime.datetime.now(), **kwargs ):
    dateobj = base + datetime.timedelta( **kwargs)
    return dateobj

def ts2unix(str_date,mask=FMT):
    return \
        int(time.mktime(
         time.strptime(str_date, mask)
        )) * 1000
    
def unix2ts(uxts,mask=FMT,base=10):
    return \
        datetime.datetime.fromtimestamp( 
         int(uxts,base)/1000 
        ).strftime(mask)

if __name__ == '__main__':    
    print ts2unix('2015-04-30')
    print unix2ts('1441422503000')
    print get_date(days=-1)
    # print str2date('2015-04-30')