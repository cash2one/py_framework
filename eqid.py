import datetime
    
def parse_eqid(eqid):
    qid=eqid[0:16]
    clusterid=eqid[16:24]
    ts=eqid[24:]
    ts=datetime.datetime.fromtimestamp( int(ts,16) ).strftime('%Y-%m-%d %H:%M:%S')    
    # print qid,clusterid,ts
    return qid,clusterid,ts
    
if __name__ == '__main__': 
    print parse_eqid('e051355e00005a4500000004558a1995')
    print parse_eqid('831e109e00000e4d0000000255ac24de')