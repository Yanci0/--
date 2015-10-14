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
        print u"����:",
        if hasattr(e,'code'):
            print e.code
        if hasattr(e,'reason'):
            print e.reason
        return ''
    except httplib.BadStatusLine:
        print u"�Բ���,����վ���ܷ���"
        return ''
    except ValueError:
        print u'��ַ��������,����������'
        return ''
    except socket.timeout:
        print u'��ʱ'
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

def add_page_to_folder(page, content): #����ҳ�浽�ļ��������ַ�Ͷ�Ӧ���ļ���д��index.txt��
    index_filename = 'index.txt'    #index.txt��ÿ����'��ַ ��Ӧ���ļ���'
    folder = 'html'                 #�����ҳ���ļ���
    filename = valid_filename(page) #����ַ��ɺϷ����ļ���
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  #����ļ��в��������½�
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)                #����ҳ�����ļ�
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
        max_page1 = int(input("������ץȡ��ҳ����:"))
        return max_page1
    except:
        print "�������, ����������"
        inputValue()

def inputValue1():
    try:
        NUM1 = int(input("�������߳���:"))
        return NUM1
    except:
        print "�������, ����������:"
        inputValue1()


Count = 1
max_page = inputValue()       #ץȡ����ҳ����
NUM = inputValue1()             #�߳���
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

