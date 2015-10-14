# -*- coding: cp936 -*-
import threading
import Queue
import time
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import urlparse
import os
import urllib
import httplib
import socket

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    try:
        req = urllib2.Request(page, None, {'User-agent' : 'Custom User Agent'})
        content = urllib2.urlopen(req,data = None, timeout = 10).read()
        return content
    except urllib2.URLError, e:
        print u"错误:",
        if hasattr(e,'code'):
            print e.code
        if hasattr(e,'reason'):
            print e.reason
        return ''
    except httplib.BadStatusLine:
        print u"对不起,此网站不能访问"
        return ''
    except ValueError:
        print u'网址输入有误,请重新输入'
        return ''
    except socket.timeout:
        print u'超时'
        return ''

def get_all_links(content, page):
    links = []
    #soup = BeautifulSoup(content)
    for i in re.findall(r'<a.*?href="(.*?)".*?<\/a>', content,re.I):#soup.findAll('a',{'href' : re.compile('^http|^/')}):
        if re.match('http',i, flags=0) == None:
            url = urlparse.urljoin(page, i)
        else:
            url = i
        links.append(url)
        #print url
    return links

def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'    #index.txt中每行是'网址 对应的文件名'
    folder = 'html'                 #存放网页的文件夹
    filename = valid_filename(page) #将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  #如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)                #将网页存入文件
    f.close()


def working():
    while True:
        global Count
        page = q.get()
        if varLock.acquire():
            print page
            varLock.release()

        if page not in crawled:
            
##        else:
##                varLock.release()
            content = get_page(page)
            outlinks = get_all_links(content, page)
            add_page_to_folder(page, content)
            
            for link in outlinks:
                Count += 1
                if Count > max_page:
                    flag = True
                    break;
                q.put(link)
                
            if varLock.acquire() and flag:
                graph[page] = outlinks
                crawled.append(page)
                varLock.release()
            q.task_done()
        else:
            q.task_done()
       

g = {'A':['B', 'C', 'D'],\
     'B':['E', 'F'],\
     'C':['1','2'],\
     '1':['3','4'],\
     'D':['G', 'H'],\
     'E':['I', 'J'],\
     'G':['K', 'L'],\
     }

def inputValue():
    try:
        max_page1 = int(input("请输入抓取网页数量:"))
        return max_page1
    except:
        print "输入错误, 请重新输入"
        inputValue()

def inputValue1():
    try:
        NUM1 = int(input("请输入线程数:"))
        return NUM1
    except:
        print "输入错误, 请重新输入:"
        inputValue1()


Count = 1
max_page = inputValue()       #抓取额网页数量
NUM = inputValue1()             #线程数
start = time.clock()

crawled = []
graph = {}
varLock = threading.Lock()
q = Queue.Queue()
q.put('http://www.sjtu.edu.cn')
for i in range(NUM):
    t = threading.Thread(target=working)
    t.setDaemon(True)
    t.start()
    
q.join()
end = time.clock()
print end-start

