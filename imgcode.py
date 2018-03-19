# -*- coding: utf-8 -*-
#author:zhousc
#Email:zhousc88@gmail.com
#purpose:制作中文验证码

from PIL import Image,ImageDraw,ImageFont
import random

class Imgcode(object):
    
    def __init__(self,width=400,height=300,fontPath = 'simkai.ttf'):
        self.height=height
        self.width=width
        self.fontPath=fontPath
        self.fontSize=60
        self.font=ImageFont.truetype(self.fontPath,self.fontSize)
        self.image=Image.new('RGB',(width,height),(255,255,255))
        
    def codetext(self):
        return(chr(random.randint(0x4E00, 0x9FBF)))
    
    def rotate(self):
        self.image.rotate(random.randint(0,50),expand=20)
     
    def drawtext(self,pos,text,fill):
        draw=ImageDraw.Draw(self.image)
        draw.text(pos,text,font=self.font,fill=fill)
    
    def randRGB(self):
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def randpoint(self):
        return (random.randint(0,self.width),random.randint(0,self.height))
    
    def randline(self,num):
        draw=ImageDraw.Draw(self.image)
        for i in range(0,num):
           draw.line((self.randpoint(),self.randpoint()),self.randRGB())
    
    def  randtext(self,num):
        start=(self.width-num*self.fontSize)/2
        for i in range(0,num):
            x=start+self.fontSize*i
            self.drawtext((x,random.randint(125,140)),self.codetext(),self.randRGB())
            self.rotate()
            self.randline(30)
      
    def savecode(self,path):
        self.image.save(path)  
            
if __name__=='__main__':
    img=Imgcode()
    img.randtext(5)
    img.savecode(r'd://code.jpeg')
    