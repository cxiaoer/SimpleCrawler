#coding:utf-8
import csv
import urllib2
# import lxml
import re
from threading import Thread
from Queue import Queue
from time import sleep
import lxml.html
import socket

"""
get the next page xpath------>[//span[@class='nextprev']/a/@href]
get the content url xpath----->[//a[@class='title may-blank ']/@href]
get the viedo link url xpath ---->[//div[@class='md']/p/a/@href]

"""
keyword_queue = Queue()
thread_num = 25
socket.setdefaulttimeout(10)

def crawl_content(keyword):
	# print Thread.getName() +" start craw keyword ----->" + keyword
	page_queue = Queue()
	main_url = "http://www.reddit.com/r/fulltvshowsonyoutube/search?q="+keyword
	page_queue.put(main_url)
	while page_queue.not_empty:
		tmp_url = page_queue.get()
		try:
			print "start crawl the main url ---->" + tmp_url
			html = urllib2.urlopen(tmp_url).read()
			dom = lxml.html.document_fromstring(html)
		except Exception, e:
			print "craw next page num error in url ---->" + tmp_url
		page_url = dom.xpath("//span[@class='nextprev']/a/@href")
		if page_url is not None:
			page_queue.put(page_url)
		content_url_list = dom.xpath("//a[@class='title may-blank ']/@href")
		for content_url in content_url_list:
			try:
				content_html = urllib2.urlopen(content_url).read()
				content_dom = lxml.document_fromstring(content_html)
				all_vimeo_links = [link for link in dom.xpath("//div[@class='md']/p/a/@href") if "vimeo" in link]
				print all_vimeo_links
			except Exception, e:
				print "craw url----------->" + content_url+" errror"


def worker():
	while keyword_queue.not_empty:
		keyword = keyword_queue.get()
		crawl_content(keyword)
		sleep(1)
		keyword_queue.task_done()


for i in thread_num:
	thread = Thread(target=worker)
	thread.setDaemon(True)
	thread.start()


def readKeyWord():
	csvRead = file("keyword.csv",'rb')
	reader = csv.reader(csvRead)
	for line in reader:
		keyword_queue.put(line[0].replace(" ","+"))

readKeyWord()
keyword_queue.join()
# crawl_content("Snooki+and+Jwoww")

