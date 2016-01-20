# -*- coding=utf-8 -*-

from urllib import *
from Tkinter import *
from tkMessageBox import *
import threading
import re
import os

info = ""
flag = False

def DownloadImage(addr):
    '''download all image from addr to new dir'''
    global info
    global flag

    try:
        url     = urlopen(addr)
        d       = os.getcwd()+os.sep+'Image'
        i       = 0
        count   = 0
        print 'begin to download,please wait...'
        for line in url:
            ls=re.findall(r'src="http:.+?jpg',line)
            for l in ls:
                if not os.path.exists(d):    
                    os.mkdir(d)
                while True:
                    filename    = '%s\\image%d.jpg' % (d,i)
                    if not os.path.exists(filename):
                        break
                    i+=1
                print l[5:]
                urlretrieve(l[5:],filename)  
                count+=1
                i+=1
    except  Exception,r:
        print r
        print 'error'
        info    = '失败了。。。提供的地址是不是贴吧帖子的。。'
    else:
        print '(%s)%d picture download succeed!' % (d,count)
        #showinfo('下载成功!','新目录创建(%s)  %d个图片被下载~' % (d,count))
        #showinfo()
        info    = '下载成功!新目录创建(%s)  %d个图片被下载~' % (d,count)
    url.close()
    flag = True
    global win
    win.event_generate("<Enter>",when="tail")
    #raw_input('any key for quit^_^')


def GetImage():
    s   = edit.get(0.0,END)
    if  s!="\n":
        showinfo('提示','开始下载,请耐心等待(别乱点= =)...')

        work    = threading.Thread(target=DownloadImage,args=(str(s),))
        work.setDaemon(True)
        work.start()
    else:
        showwarning('你想干啥...','请输入网页地址!')

def show(arg):
    global flag,info
    if flag:
        showinfo('提示',info)
        flag    = False
        info    = ''


if __name__=="__main__":
    win     = Tk()
    win.title('贴吧图片下载器')
    win.geometry('220x120+700+300')
    win.wm_attributes('-topmost',True)
    label   = Label(win, text='输入网页的地址:')
    label.pack()#side='left')
    edit    = Text(win,width=30,height=3,borderwidth=2)
    edit.pack()
    button  = Button(win,text='点击开始下载',command=GetImage)
    button.pack()
    win.bind("<Enter>",show)
    win.mainloop()

