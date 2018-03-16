#author: zhousc

import os
import random
import sys
import tkinter
import xlrd
import xlwt

#公司年会上的抽奖
def goodman():
    if people_list :
        goodman=random.choice(people_list)
        people_list.remove(goodman)
    else:
        goodman="请输入人员名单"
    l['text']=goodman

if __name__=="__main__":
    top=tkinter.Tk()
    top.title("年会抽奖")
    top.geometry('500x300')
    people_list=[1] #参与抽奖的名单
    l=tkinter.Label(top,text='', width=15, height=10,font=(30))
    tkinter.Button(top,text="开奖",command=goodman,width=10,height=4).pack()
    l.pack(side='top')
    top.mainloop()