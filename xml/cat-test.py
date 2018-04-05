import shutil,os,sys
from lxml import etree




root=r'D:\code\company_svn_2nd\testbak'
rootdirs=[root+'\\service',root+'\\web']
web_filters=['gw-web-bank-receive','gw-web-gateway','gw-web-rcms']
service_filters=['gw-service-account','gw-service-bank','gw-service-banklink','gw-service-boss','gw-service-cost']

for i,mydir in enumerate(rootdirs):
    flist=os.listdir(mydir)
    state = 'service' if i==0 else 'web'
    for fname in flist:
        if (fname not in web_filters) and (fname not in service_filters):
            continue
        fpath=os.path.join(mydir,fname)
        # log4j.properties
        log4j=os.path.join(fpath,'src/main/resources/log4j.properties')
        if os.path.exists(log4j):
            with open(log4j,'r+',encoding='utf-8') as logf:
                lines=logf.readlines()
                find_cat=False
                last_appender_index=0
                for i,line in enumerate(lines[:]):
                    if line.find('log4j.rootLogger')!=-1 and line.find('Cat')<0:
                        lines[i]=line.strip()+",Cat\n"
                    if line.find('log4j.appender.Cat') !=-1:
                        find_cat=True
                        # break
                    if line.find('log4j.appender.') !=-1:
                        last_appender_index=i

                if not find_cat and last_appender_index>0:
                    lines.insert(last_appender_index+1,'\n# cat\nlog4j.appender.Cat=com.dianping.cat.log4j.CatAppender\n')
                    for j,line in enumerate(lines[:]):
                        if line.find('log4j.logger.')>=0 and line.find('Cat')<0:
                            lines[j]=line.strip()+",Cat\n"

                with open(log4j,'w',encoding='utf-8') as logf2:
                    logf2.writelines(lines)
