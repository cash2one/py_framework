import itertools
# itertools.permutations(arr)
# itertools.combinations(arr)
# itertools.product(arr,[2,1])
def get_input():
    print "Usage:','split array('#'fake split,'>'sub split)"
    input_str="factory_id#factory_name,series_id>spec_id>object_id"
    input_str="2>3,4>5"
    input_str="platform>app_soft_type>app_sys_type,pvareaid#pvarea_name,province_id#province_name>city_id#city_name,bussiness_type,dealer_id#dealer_name,brand_id#brand_name>series_id#series_name>spec_id#spec_name>item_id#item_name"
    # input_str="brand_id#brand_name>series_id#series_name>spec_id#spec_name>object_id"
    # input_str=raw_input("array: ")
    input_str='platform>app_soft_type>app_sys_type,pvareaid#pvarea_name,province_id#province_name>city_id#city_name'
    input_arr=input_str.split(',')
    return input_arr,input_str
    
def parse_input_arr(input_arr):
    rollup_groups=[]
    need_pop=[]
    for i,element in enumerate(input_arr):
        if element.find('>')!=-1:
            ruarr=element.split('>')
            group_s=[]
            for j in range(len(ruarr)+1):
                group=[]
                for part in ruarr[:j]:
                    # print part
                    group.append(part)
                # print group
                group_s.append(group)
            rollup_groups.append(group_s)
            need_pop.insert(0,i)
    for i in need_pop:
        input_arr.pop(i)
    # print 'input_arr:',input_arr  
    # print 'rollup_groups:',rollup_groups  
    return input_arr,rollup_groups
        
def expand_rollup(rollup_groups):
    def joinlist(x,y):
        for ey in y:
            x.append(ey)
        return x
    expand=[reduce(joinlist,el,list()) for 
        el in itertools.product(*rollup_groups)]
    return expand
    
def star_product(iter1,iter2_s):    
    ex_iter2=expand_rollup(iter2_s)
    if len(iter1)==0:
        for e2 in ex_iter2:
            if len(e2)==0:continue
            yield tuple(e2)
    for e1 in iter1:
        for e2 in ex_iter2:
            # print e1,e2
            le1=list(e1)
            le1.extend(e2)
            # print le1
            yield tuple(le1)
    
        
def output(input_arr,rollup_groups,input_str):    
    ret_arr=[]
    for i in range(len(input_arr)+1,0,-1):
        iter=[e for e in itertools.combinations(input_arr,i)]
        # print 'iter',iter
        if len(rollup_groups)>0:
            iter=star_product(iter,rollup_groups)
        ret_arr.extend( [el for el in iter] )
    # print 'ret_arr:',ret_arr
    print '#'*20
    print 'group by ',input_str.replace('>',',').replace('#',',')
    print 'grouping sets '
    print str( tuple(ret_arr) ).replace("'","").replace(",)",")").replace("#",",") .replace("), (","),\n(")
    
if __name__=='__main__':
    input_arr,input_str=get_input()
    input_arr,rollup_groups=parse_input_arr(input_arr)
    output(input_arr,rollup_groups,input_str)
    # print expand_rollup([ [[],[1],[1,2]] , [[],[3],[3,4]] ,[[],[5],[5,6]]])
    # for k in star_product(['1'],[ [[],[1],[1,2]] , [[],[3],[3,4]] ,[[],[5],[5,6]]]):
        # print k