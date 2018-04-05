import shutil,os,sys
from lxml import etree




root=r'D:\code\company_svn_2nd\dev'
rootdirs=[root+'\\service',root+'\\web']
web_filters=['gw-web-bank-receive','gw-web-gateway','gw-web-rcms']
service_filters=['gw-service-account','gw-service-bank','gw-service-banklink','gw-service-boss','gw-service-cost']

def processService(fpath):
    if not os.path.exists(fpath):
        return
    parser = etree.XMLParser(remove_blank_text=True)
    xml=etree.parse(fpath,parser)    
    root=xml.getroot()
    ns='{%s}' % root.nsmap[None]

    find_cat=False
    sqlSessionFactory=root.find('{0}bean[@id="sqlSessionFactory"]'.format(ns))
    if sqlSessionFactory.find('{0}property[@name="plugins"]'.format(ns)) is None:
        sqlSessionFactory.append(etree.XML('''
        <property name="plugins">
			<array>
				<bean class="com.dianping.cat.plugins.CatMybatisPlugin"></bean>
			</array>
		</property>
        '''))
    el=etree.ElementTree(root)
    el.write(fpath,encoding='utf-8',pretty_print=True)

def processWeb(fpath):
    parser = etree.XMLParser(remove_blank_text=True)
    xml=etree.parse(fpath,parser)    
    root=xml.getroot()
    ns='{%s}' % root.nsmap[None]

    find_cat=False
    first_filter=root.find('{0}filter'.format(ns))
    for node in root.findall('{0}filter/{0}filter-name'.format(ns)):
        if node.text=='cat-filter':
            find_cat=True

    if not find_cat:
        first_filter.addprevious(etree.XML('''
    <filter>
		<filter-name>cat-filter</filter-name>
		<filter-class>com.dianping.cat.servlet.CatFilter</filter-class>
	</filter>
        '''))
        first_filter.addprevious(etree.XML('''
    <filter-mapping>
		<filter-name>cat-filter</filter-name>
		<url-pattern>/*</url-pattern>
		<dispatcher>REQUEST</dispatcher>
		<dispatcher>FORWARD</dispatcher>
	</filter-mapping>
        '''))
    el=etree.ElementTree(root)
    el.write(fpath,encoding='utf-8',pretty_print=True)

def processPom(fpath):
    parser = etree.XMLParser(remove_blank_text=True)
    xml=etree.parse(fpath,parser)    
    root=xml.getroot()
    ns='{%s}' % root.nsmap[None]
    find_cat_dep=False
    find_cat_res=False

    for node in root.findall('{0}dependencies/{0}dependency'.format(ns)):
        artifactId=node.find('{0}artifactId'.format(ns)).text
        if artifactId=='cat-plugin':
            find_cat_dep=True
            break

    if not find_cat_dep:
        deps=root.find('{0}dependencies'.format(ns))
        dept=etree.SubElement(deps,'dependency')
        groupId=etree.SubElement(dept,'groupId')
        groupId.text="com.gw"
        artifactId=etree.SubElement(dept,'artifactId')
        artifactId.text="cat-plugin"
        version=etree.SubElement(dept,'version')
        version.text="1.0"

    for node in root.findall('{0}build/{0}plugins/{0}plugin/{0}configuration/{0}webResources/{0}resource'.format(ns)):
        if node.find('{0}directory'.format(ns)).text=='deploy/${env}/META-INF':
            find_cat_res=True
            break

    res=root.find('{0}build/{0}plugins/{0}plugin/{0}configuration/{0}webResources'.format(ns))
    if not find_cat_res and res is not None:
        myres=etree.SubElement(res,'resource')
        directory=etree.SubElement(myres,'directory')
        directory.text="deploy/${env}/META-INF"
        targetPath=etree.SubElement(myres,'targetPath')
        targetPath.text="WEB-INF/classes/META-INF"

    el=etree.ElementTree(root)
    el.write(fpath,encoding='utf-8',pretty_print=True)

for i,mydir in enumerate(rootdirs):
    flist=os.listdir(mydir)
    state = 'service' if i==0 else 'web'
    for fname in flist:
        if (fname not in web_filters) and (fname not in service_filters):
            continue
        fpath=os.path.join(mydir,fname)
        pomfile=os.path.join(fpath,'pom.xml')
        # pom.xml for dev change
        processPom(pomfile)
        # app.properties
        app_prop_dir=os.path.join(fpath,'src/main/resources/META-INF')
        if not os.path.exists(app_prop_dir):
            os.makedirs(app_prop_dir,exist_ok=True)
            with open(os.path.join(app_prop_dir,'app.properties'),'w+',encoding='utf-8') as appf:
                appf.write('app.name=%s' % fname)
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

        # web
        if state=='web':
            web_xml=os.path.join(fpath,'src/main/webapp/WEB-INF/web.xml')
            processWeb(web_xml)
        # mybatis
        else:
            mybatis=os.path.join(fpath,'src/main/resources/spring/spring-mybatis.xml')
            processService(mybatis)
        