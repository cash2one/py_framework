import re

import json
import glob

DEBUG=False
    
def download_projects_zipfile(aa):    
    for prj in get_projects(aa):
        aa.download_project(prj)
   
def get_job_nodes(aa,project):    
    aa.set_project(project)
    # aa.manager_cmd('ffe','ads_1111__1130hour_noop')
    flows=aa.manager_cmd('fpf')['flows']
    for flowinfo in flows:
        # break
        flow=flowinfo['flowId']        
        jo= aa.manager_cmd('ffg',flow)
        nodes= jo['nodes']
        for node in nodes:
            print project,node['id'],node['type'],",".join(node.get('in',''))        

def get_projects(aa):
    projects=aa.fetch_project_list()    
    for project in projects:
        yield project
    
def list_all_jobs(aa):
    for project in get_projects(aa):
        get_job_nodes(aa,project)
    
def extract_zip_project(project):
    import zipfile
    content={}
    zf=zipfile.ZipFile('data/%s.zip'%project)
    if DEBUG:print zf,dir(zf)
    for file in zf.filelist:
        if DEBUG: print file,file.orig_filename
        if DEBUG: print dir(file)
        fname=file.orig_filename
        ct=zf.read(fname)
        # print ct
        content[fname]= ct
    return content

    
def get_dependence_from_cmd(content):
    deps=[]
    PAT=re.compile(r'command(\.\w)?\=\${checkfile} -t A -table (\w*).*')    
    PAT2=re.compile('outer.dependencies=([\w\.,]*)')
    for l in content.split('\n'):
        m=PAT.match(l)
        if m:
            dep= m.group(2)
            deps.append(dep)
            continue
        m=PAT2.match(l)
        if m:
            dep= m.group(1)
            deps.extend(dep.split(',') )
            continue
    return deps
        
def get_dependence_from_zip(project):
    content=extract_zip_project(project)
    for fname in content:
        tname=fname.split('/')[-1].split('.')[0]
        if tname in ('env'):
            continue
        depend=get_dependence_from_cmd(content[fname])
        print '\t'.join([project,tname,','.join(depend)])
    
if __name__=='__main__':
    import optparse,sys,AzkabanAPI
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', action="store_true", dest="debug", help="debug", default=False)
    opts, args = parser.parse_args()
    
    DEBUG=opts.debug
    
    aa=AzkabanAPI.AzkabanAPI('http://192.168.223.32:8070')
    # aa=AzkabanAPI.AzkabanAPI('https://192.168.201.58:8443')
    aa.login(username='dw',password='EA870442-FBA9-4539-A9AE-06EF982AB13D')
    
    # download_projects_zipfile(aa)
    for project in get_projects(aa):
        print project
        content=get_dependence_from_zip(project)