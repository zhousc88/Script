#author:zhousc
#E-mail:zhousc88@gmail.com
#purpose:年度考勤资料整理

import os
import xlrd
import xlwt
from datetime import date,datetime

def add_time(time1,time2):
    p=time1.split(':')
    p1=time2.split(':')
    p[2]=int(p[2])+int(p1[2])
    if p[2]>=60:
        p[2]=p[2]-60
        p[1]=int(p[1])+int(p1[1])+1
        if p[1]>=60:
            p[1]=p[1]-60
            p[0]=int(p[0])+int(p1[0])+1
        else:
            p[0]=int(p[0])+int(p1[0])
    else:
        p[1]=int(p[1])+int(p1[1])
        if p[1]>=60:
            p[1]=p[1]-60
            p[0]=int(p[0])+int(p1[0])+1
        else:
            p[0]=int(p[0])+int(p1[0])
    p=[str(i) for i in p]
    return ":".join(p)
    
if __name__=='__main__':
    path=r'C:\Users\Administrator\Desktop\考勤'
    files=os.listdir(path)
    filename=os.path.join(path,files[0])
    book=xlrd.open_workbook(filename)
    sheet=book.sheet_by_name("苏州")
    work=[]
    for i in range(2,sheet.nrows):
        name=sheet.cell(i,1).value
        temp=sheet.cell(i,3).value
        work_time={name:temp}
        work.append(work_time)
    for i in range(1,len(files)):
        filename=os.path.join(path,files[i])
        book=xlrd.open_workbook(filename)
        print(filename)
        sheet=book.sheet_by_name("苏州")
        for i in range(2,sheet.nrows):
            exist=True
            name=sheet.cell(i,1).value
            temp=sheet.cell(i,3).value
            for j in work:
                if name in j:
                    j[name]=add_time(j[name],temp)
                    exist=False
            if exist:
                work.append({name:temp})
    work_book=xlwt.Workbook()
    sheet1=work_book.add_sheet('苏州',cell_overwrite_ok=True)
    sheet1.write(0,0,'姓名')
    sheet1.write(0,1,'加班时间')
    for i in range(len(work)):
        name=work[i].popitem()
        sheet1.write(i+1,0,name[0])
        sheet1.write(i+1,1,name[1])
    work_book.save(r"C:\Users\Administrator\Desktop\1.xls")

       
        
