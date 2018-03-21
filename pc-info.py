# -*- coding: utf-8 -*-
#authour:zhousc
#Email:zhousc88@gmail.com
from subprocess import Popen,PIPE
import re
def getinfo():
    ipcmd=Popen(['ipconfig','/all'],stdout=PIPE)
    data=ipcmd.stdout.read().decode('gb2312')
    lines=data.split('\n')
    macs=set()
    for line in lines:
        if line.startswith(' '):
            if '主机名'in line:
                pcname=re.compile(': (\S+)').findall(line)
            if '物理地址' in line :
                mac=re.compile(': (\S+)').findall(line).pop()
                macs.add(mac)
            if 'IPv4 地址' in  line:
                ip=re.compile('((\d+).(\d+).(\d+).(\d+))').search(line).group()
    syscmd=Popen(['systeminfo'],stdout=PIPE)
    systemdata=syscmd.stdout.read().decode('gb2312')
    syslines=systemdata.split('\n',)
    os_list=[]
    for line in syslines:
        if not line.startswith(' '):
            if 'OS 名称'in line:
                osname=re.compile('   (.*)\\r').search(line).group().lstrip().strip()
            if 'OS 版本'in line:
                osversions=re.compile('   (.*)').search(line).group().lstrip().strip()
                os_list.append(osversions)
            if '产品 ID'in line:
                osid=re.compile('   (.*)').search(line).group().lstrip().strip()
            if '系统型号'in line:
                ostype=re.compile('   (.*)').search(line).group().lstrip().strip()
            if '物理内存总量'in line:
                memory=re.compile('   (.*)').search(line).group().lstrip().strip()
                memory=memory.rstrip()
    info={'name':pcname.pop(),'mac':macs,'ip4':ip,'osname':osname,'osversions':os_list,'osid':osid,'ostype':ostype,'memory':memory}
    return info
if __name__=='__main__':
    info=getinfo()
    print(info)