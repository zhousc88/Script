#author: zhousc
#email:zhousc88@gmail.com
#图片制作成ICO

import os
import sys
from PIL import Image

if __name__=='__main__':
    path=r'C:\Users\Administrator\Desktop\Export'
    files=os.listdir(path)
    size=256
    for file in files:
        filename=os.path.join(path,file)
        name=file.split('.')[:-1].pop()
        iconame=name+'.ico'
        print(iconame)
        f=Image.open(filename)
        f.resize((size,size),Image.ANTIALIAS).save(os.path.join(path,iconame))