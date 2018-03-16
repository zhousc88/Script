# -*- coding: utf-8 -*-
# @Author: zhousc
# @Time: 2017-4-27 16:16
# Email:zhousc88@gmail.com
#purpose:百度上下载图片

import urllib
import requests
import os
import re
import sys
import time
import threading
from datetime import datetime as dt
from multiprocessing.dummy import Pool
from multiprocessing import Queue

class BDdownloader(object):
    str_table = {
        '_z2C$q': ':',
        '_z&e3B': '.',
        'AzdH3F': '/'
    }

    char_table = {
        'w': 'a',
        'k': 'b',
        'v': 'c',
        '1': 'd',
        'j': 'e',
        'u': 'f',
        '2': 'g',
        'i': 'h',
        't': 'i',
        '3': 'j',
        'h': 'k',
        's': 'l',
        '4': 'm',
        'g': 'n',
        '5': 'o',
        'r': 'p',
        'q': 'q',
        '6': 'r',
        'f': 's',
        'p': 't',
        '7': 'u',
        'e': 'v',
        'o': 'w',
        '8': '1',
        'd': '2',
        'n': '3',
        '9': '4',
        'c': '5',
        'm': '6',
        '0': '7',
        'b': '8',
        'l': '9',
        'a': '0'
    }

    re_objURL = re.compile(r'"objURL":"(.*?)".*?"type":"(.*?)"')
    re_downNum = re.compile(r"已下载\s(\d+)\s张图片")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, sdch",
    }
    def __init__(self, word, dirpath=None, processNum=30):
        if " " in word:
            raise AttributeError("脚本只支持单个关键字")
        self.word = word
        self.char_table = {ord(key):ord(value)
                           for key ,value in BDdownloader.char_table.items()}
        if not dirpath:
            dirpath = os.path.join(sys.path[0],word)
        self.dirpath = dirpath
        self.jsonURLFile = os.path.join(sys.path[0],word+'jsonUrl.txt')
        self.logFile = os.path.join(sys.path[0],word+'lonInfo.txt')
        self.errorFile = os.path.join(sys.path[0],word+'errorUrl.txt')
        if os.path.exists(self.errorFile):
            os.remove(self.errorFile)
        if not os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)
        self.pool = Pool(30)
        self.session = requests.Session()
        self.session.headers =BDdownloader.headers
        self.queue = Queue()
        self.messageQueue = Queue()
        self.index = 0
        self.promptNum =10
        self.lock =threading.Lock()
        self.delay = 1.5
        self.QUIT= "QUIT"
        self.printPrefix ="##"

    def start(self):
        t = threading.Thread(target=self.__log)
        t.setDaemon(True)
        t.start()
        self.messageQueue.put(self.printPrefix+"开始运行")
        start_time = dt.now()
        urls = self.__buildUrls()
        self.messageQueue.put(self.printPrefix+"已获取%s个请求地址"%len(urls))
        self.pool.map(self.__resolveImgUrl, urls)
        while self.queue.qsize():
            imgs = self.queue.get()
            self.pool.map_async(self.__downImg, imgs)
        self.pool.close()
        self.pool.join()
        self.messageQueue.put(self.printPrefix+"下载完成！已下载%s张图片，总用时 %s"%(self.index,dt.now() - start_time))
        self.messageQueue.put(self.printPrefix+"请到%s查看结果"%self.dirpath)
        self.messageQueue.put(self.printPrefix+"报错信息保存在%s"%self.errorFile)
        self.messageQueue.put(self.QUIT)

    def __log(self):
        with open(self.logFile, "w",encoding="utf-8") as f:
            while True:
                message = self.messageQueue.get()
                if message == self.QUIT:
                    break
                message =str(dt.now()) + " " + message
                if self.printPrefix in message:
                    print(message)
                elif "已下载" in  message:
                    downNum = self.re_downNum.findall(message)
                    if downNum and int(downNum[0]) % self.promptNum == 0:
                        print(message)
                    f.write(message + '\n')
                    f.flush()

    def __getIndex(self):
        self.lock.acquire()
        try:
            return self.index
        finally:
            self.index += 1
            self.lock.release()

    def decodeurl(self,url):
        for key,value in self.str_table.items():
            url = url.replace(key,value)
        return url.translate(self.char_table)

    def __buildUrls(self):
        word = urllib.parse.quote(self.word)
        url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
        time.sleep(self.delay)
        html =self.session.get(url.format(word=word,pn=0),timeout = 15).content.decode('utf-8')
        results = re.findall(r'"displayNum":(\d+),',html)
        maxNum = int(results[0]) if results else 0
        urls = [url.format(word=word,pn=x) for x in range(0,maxNum+1,60)]
        with open(self.jsonURLFile,"w",encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        return  urls

    def __resolveImgUrl(self,url):
        time.sleep(self.delay)
        html = self.session.get(url,timeout =15).content.decode('utf-8')
        datas = self.re_objURL.findall(html)
        imgs = [Image(self.decodeurl(x[0]),x[1]) for x in datas]
        self.messageQueue.put(self.printPrefix+"已经解析出%s个图片地址"%len(imgs))
        self.queue.put(imgs)

    def __downImg(self, img):
        imgUrl = img.url
        try:
            time.sleep(self.delay)
            res = self.session.get(imgUrl, timeout=15)
            message = None
            if str(res.status_code)[0] == "4":
                message = "\n%s： %s" % (res.status_code, imgUrl)
            elif "text/html" in res.headers["Content-Type"]:
                message = "\n无法打开图片： %s" % imgUrl
        except Exception as e:
            message = "\n抛出异常： %s\n%s" % (imgUrl, str(e))
        finally:
            if message:
                self.messageQueue.put(message)
                self.__saveError(message)
                return
        index = self.__getIndex()
        self.messageQueue.put("已下载 %s 张图片：%s" % (index + 1, imgUrl))
        filename = os.path.join(self.dirpath,self.word+str(index) + "." + img.type)
        with open(filename, "wb") as f:
            f.write(res.content)
    def __saveError(self,message):
        self.lock.acquire()
        try:
            with open(self.errorFile, "a",encoding="utf-8") as f:
                f.write(message)
        finally:
            self.lock.release()

class Image(object):
    def __init__(self, url, type):
        super(Image, self).__init__()
        self.url = url
        self.type = type

if __name__ == '__main__':
    print("欢迎使用百度图片下载脚本！\n目前仅支持单个关键词。")
    print("下载结果保存在脚本目录下的同名文件夹中。")
    print("=" # 50)
    word =input("请输入关键词：\n")
    down = BDdownloader(word)
    down.start()