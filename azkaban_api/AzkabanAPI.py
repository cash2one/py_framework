import requests
import re

DEBUG=False

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass
    
class AzkabanAPI():
    def __init__(self,host):
        self.host=host
        self.project=''
        
    def set_project(self,project):    
        self.project=project
        
    def add_common_prop(self,data):
        cdata=data
        if not 'session.id' in data:
            cdata['session.id']=self.session_id
        if not 'project' in data:
            cdata['project']=self.project
        return cdata
        
    def get(self,url,data):
        data=self.add_common_prop(data)
        # print '[data :%s]'%data
        r=requests.get(self.host+url,data, verify=False)
        if r.headers['Content-Type']=='application/json':        
            jo= r.json()
            # print json.dumps(jo,indent=2)
            return jo
        else:
            return r
        
    def post(self,url,data):
        r=requests.post(self.host+url,data, verify=False)
        return r
        
    def login(self,username='',password=''):
        data={'action':'login','username':username,'password':password}
        r=self.post('/?action=login',data)
        # print r.text
        self.session_id= r.json()['session.id']
        if DEBUG:print 'login success'
        return r.json()['session.id']
        
    def fetch_project_list(self):    
        data={'session.id':self.session_id}
        projs=[]
        pat=re.compile(r'"/manager\?project=(\w*)"')
        r=self.get('/index',data)
        # print r.text
        for l in r.text.split('\n'):
            m=pat.search(l)
            if m:
                proj=m.group(1)
                # print proj
                projs.append(proj) 
        return projs
        
    def download_project(self,project,folder='data'):
        import os
        if not os.path.exists(folder):os.mkdir(folder)
        data={'project':project}
        r=self.get('/manager?download=true',data)
        with open('%s/%s.zip'%(folder,project),'wb') as fh:
            fh.write(r.content)
        return r
    
    def manager_cmd(self,cmd_opt,flow=None,start=0,length=5):
        options={'fpf':'fetchprojectflows',
        'ffg':'fetchflowgraph','ffe':'fetchFlowExecutions'}
        cmd=options.get(cmd_opt,'')
        data={'ajax':cmd,}
        if flow!=None:
            data['flow']=flow
        if cmd=='fetchFlowExecutions':
            data.update({'start':start,'length':length})
        r=self.get('/manager',data)
        if DEBUG: print '[manager called: %s]'%cmd,data.get('flow',''),data.get('project','')
        return r
        
    def executor_cmd(self,cmd_opt,flow=None,execid=None,idata=None):
        options={'gr':'getRunning','fef':'fetchexecflow',
            'pf':'pauseFlow','cf':'cancelFlow',
            'sf':'scheduleFlow','usf':'removeSched',
            'ef':'executeFlow','rf':'resumeFlow',
            'fejl':'fetchExecJobLogs','fefu':'fetchexecflowupdate'}
        cmd=options.get(cmd_opt,'')
        data={'ajax':cmd,}
        if execid!=None:
            data['execid']=execid
        if flow!=None:
            data['flow']=flow
        if idata!=None:
            data.update(idata)
        if DEBUG: print '[executor called: %s]'%cmd,data.get('flow',''),data.get('project','')
        r=self.get('/executor',data)
        return r 
    
    def fetch_exec_id(self,execid):
        jobs=self.executor_cmd('fef',execid=execid)
        print jobs
        # return
        for job in jobs['nodes']:
            if job['status']!='RUNNING':
                continue
            r=self.executor_cmd('fejl',execid=execid,
                idata={'jobId':job['id'],'offset':0,'length':100})
            try:
                jo=r.json()
            except:
                print r,job['status']
            for l in jo['data'].split('\n'):
                print l

if __name__=='__main__':
    pass