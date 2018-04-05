import shutil,os,sys
from lxml import etree

root=r'D:\code\company_svn_2nd\preprod'
rootdirs=[root+'\\service',root+'\\web']
web_filters=['gw-web-bank-receive','gw-web-gateway','gw-web-rcms']
service_filters=['gw-service-account','gw-service-bank','gw-service-banklink','gw-service-boss','gw-service-cost']

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
    if not find_cat_res and res:
        myres=etree.SubElement(res,'resource')
        directory=etree.SubElement(myres,'directory')
        directory.text="deploy/${env}/META-INF"
        targetPath=etree.SubElement(myres,'targetPath')
        targetPath.text="WEB-INF/classes/META-INF"

    for node in root.findall('{0}build/{0}resources/{0}resource'.format(ns)):
        if node.find('{0}directory'.format(ns)).text=='deploy/${env}':
            find_meta=False
            if node.find('{0}includes'.format(ns)) is None:
                continue
            for include_node in node.findall('{0}includes/{0}include'.format(ns)):
                if include_node.text.find('META-INF')==0:
                    find_meta=True
                    break
            if not find_meta:
                node.find('{0}includes'.format(ns)).append(etree.XML('''
                    <include>META-INF/**/*.*</include>
                '''))


    el=etree.ElementTree(root)
    el.write(fpath,encoding='utf-8',pretty_print=True)

def processCatClientXml(fpath):
    if not os.path.exists(fpath):
        return
    
    cat_dir=os.path.join(fpath,'META-INF/cat')
    cat_file=os.path.join(cat_dir,'client.xml')
    if os.path.exists(cat_file):
        return
    os.makedirs(cat_dir,exist_ok=True)
    with open(cat_file,'w+',encoding='utf-8') as catf:
        catf.write('''<?xml version="1.0" encoding="utf-8"?>
<config mode="client" xmlns:xsi="http://www.w3.org/2001/XMLSchema" xsi:noNamespaceSchemaLocation="config.xsd">
	<servers>
		<server ip="10.20.29.108" port="2280" http-port="8181" />
		<server ip="10.20.29.104" port="2280" http-port="8181" />
		<server ip="10.20.29.101" port="2280" http-port="8181" />
	</servers>
</config>
        ''')
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

        # copy cat client.xml
        deploy_dir=os.path.join(fpath,'deploy')
        if os.path.exists(deploy_dir):
            joinpay=os.path.join(deploy_dir,'joinpay')
            joinpay2=os.path.join(deploy_dir,'joinpay2')
            processCatClientXml(joinpay)
            processCatClientXml(joinpay2)