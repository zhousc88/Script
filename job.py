#!/usr/bin/python
# -*- coding: utf-8 -*-
#author:zhousc
#Email:zhousc88@gmail.com
#prupose:智联职位搜索

import os
import re
import requests
import sys
import urllib
import xlwt

if __name__=="__main__":
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheet',cell_overwrite_ok=True)
    word = input("请输入关键字：\n")
    pat1=[]
    pat2=[]
    pat3=[]
    pat4=[]
    pat5=[]
    pat6=[]
    for j in range(1,6):
        url="http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E8%8B%8F%E5%B7%9E&kw={word}&isadv=0&sg=b0a0fd499b4a4c0aae3e160b8addbbdc&p={p}"
        #html = request.urlopen("http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E8%8B%8F%E5%B7%9E&kw=python&isadv=0&sg=b0a0fd499b4a4c0aae3e160b8addbbdc&p="+str(j)).read()
        html=requests.get(url.format(word=word,p=str(j))).content.decode("utf-8")
        part1='onclick="submitLog.*?">(.*?)</a>'
        part2='<td class="gsmc"><a href="(.*?)" target='
        part3='<td class="zwyx">(.*?)</td>'
        part4='<td class="gzdd">(.*?)</td>'
        part5='target="_blank">(.*?)<'
        part6='li class="newlist_deatil_last">(.*?)</li></li>'

        pat1.extend(re.compile(part1).findall(html))
        pat2.extend(re.compile(part2).findall(html))
        pat3.extend(re.compile(part3).findall(html))
        pat4.extend(re.compile(part4).findall(html))
        pat5.extend(re.compile(part5).findall(html,))
        pat6.extend(re.compile(part6).findall(html))
    k=0
    for i in range(0,len(pat1)):
            sheet.write(i+1,k,pat1[i])
            sheet.write(i+1,k+1,pat2[i])
            sheet.write(i+1,k+2,pat3[i])
            sheet.write(i+1,k+3,pat4[i])
            sheet.write(i+1,k+4,pat5[i])
            sheet.write(i+1,k+5,pat6[i])

    #book.save('d:\\zhousc\qiuzhi.xls')
    book.save(os.path.join(sys.path[0],word+".xls"))

