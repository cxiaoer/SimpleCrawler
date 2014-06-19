#coding:utf-8
#爬取百度贴吧上的带有百度网盘和酷盘链接，丢到csv中
import urllib2
import re
import csv
from lxml import *
import lxml.html
from urllib2 import HTTPError
import threading
import socket




threadListXpath = "//*[@id='frs_list_pager']/a"
singleThreadBaseXpath = "//*[@id='thread_list']/li[$]/div/div[2]/div[1]/div[1]/a"
# postListXpath = "//*[@id='thread_theme_7']/div[1]/ul"
# pageNum = "//*[@id='thread_theme_7']/div[1]/ul/li[2]/span[2]"


baseUrl = "http://tieba.baidu.com"
basePageUrl = "http://tieba.baidu.com/f?kw=%B1%AC%D1%AA%C9%EE%C7%EF&pn="
initUrl = "http://tieba.baidu.com/f?kw=%B1%AC%D1%AA%C9%EE%C7%EF&pn=0"

# html = urllib2.urlopen(initUrl,timeout=15).read().decode('gbk')
#
# doc = lxml.html.document_fromstring(html)
# l = doc.xpath(threadListXpath)

def main(start,end,writer):
    i = start
    while i < end:
        print "start the "+repr(i*50)+"nd page!"
        doc = httpRequest(basePageUrl+repr(i*50))
        threadList = doc.xpath("//a[@class='j_th_tit']/@href")
        for singleBaseThreadUrl in threadList:
            singleThreadUrl = baseUrl+singleBaseThreadUrl
            getThreadLink(singleThreadUrl,writer)
        i+=1

        # j = 1
        # while j <= 49:
        #     if j==1 and i==0:
        #         j = j+ 1
        #         continue
        #     d = doc.xpath("//a[@class='j_th_tit']/@href")
        #     for e in d:


        #     newUrl = baseUrl+d[0].get('href')
        #     print "start enter into the post url ＝ "+ newUrl
        #     getThreadLink(newUrl,writer)
        #     j =j+1
        # i=i + 1
    



def getThreadLink(url,writer):
    # html = urllib2.urlopen(url).read().decode('gbk')
    # doc = lxml.html.document_fromstring(html)
    doc = httpRequest(url)
    if doc == None:
        return
    pageNum = doc.xpath("//*[@id='thread_theme_7']//li[@class='l_reply_num']/span[2]/text()")
    if len(pageNum) == 0:
        return
    # print pageNum[0].get('text')
    print "url ="+url+" has "+repr(pageNum[0])+"posts list!"
    i = 1
    while i <= int(pageNum[0]):
        nextPostListUrl = url+"?pn="+repr(i)
        print "it is on "+nextPostListUrl
        tmpDoc = httpRequest(nextPostListUrl)
        if tmpDoc == None:
            continue
        findLinkSite(tmpDoc,nextPostListUrl,writer)
        i+=1



def findLinkSite(doc,url,writer):
    list = doc.xpath("//div[@class='p_content p_content_nameplate']/cc//a/text()")
    for l in list:
        if "pan.baidu.com" in l or "kupan.cc" in l:
            print "find linking url in "+url+" with " + l
            writer.writerow([url,l])

def httpRequest(url):
    try:
        html = urllib2.urlopen(url).read()
        doc = lxml.html.document_fromstring(html)
        return doc
    except HTTPError as e:
        print e
    except UnicodeDecodeError as e:            
        print('-----UnicodeDecodeError url:',url)        
    except socket.timeout as e:  
        print("-----socket timout:",url)


def multiMain():
    timeout = 10
    socket.setdefaulttimeout(timeout)
    csvWrite = open('/home/vobile/Documents/tieba1.csv',"w+")
    writer = csv.writer(csvWrite,quoting=csv.QUOTE_ALL)
    main(0,5,writer)
    csvWrite.close()


multiMain()
