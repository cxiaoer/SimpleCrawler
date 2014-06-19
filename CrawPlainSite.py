#coding:utf-8
import csv
import urllib2
import re
from HTMLParser import HTMLParser



class myHtmlParser(HTMLParser):
	"""docstring for myHtmlParser"""
	def __init__(self):
		HTMLParser.__init__(self)
		self.links =[]
		self.flag = 0
	def handle_starttag(self,tag,attrs):

		if tag == "a":
			if len(attrs) == 0:
				pass
			else:
				for (variable, value) in attrs:
					if variable == "rel":
#							print attrs[1][1]
							self.links.append(attrs[1][1])
							# print attrs
							# print "hello"
							# self.links.append(attrs['href'])
							# break
		
		
csvRead = file('putlockerhosting.csv','rb')
reader = csv.reader(csvRead)
csvWrite = open('result.csv',"wb")
writer = csv.writer(csvWrite,quoting=csv.QUOTE_ALL)
# url_pat = re.compile(r'<td class="entry" width="100%">(.*?)<td>')
head = ['Display Title','index url','hosting url']
writer.writerow(head)
for line in reader:
	if reader.line_num == 1:
		continue
	print line[1].strip()
	hp = myHtmlParser()
	content = urllib2.urlopen(line[1]).read()
	hp.feed(content)
	# print siteUrl = re.findall(url_pat,content)
	hp.close()
	siteUrl = []
	for i in hp.links[1:]:
		if i not in siteUrl:
			print i
			siteUrl.append(i)
	# writer = csv.writer(open('result.csv',"wb"),quoting=csv.QUOTE_ALL)
	for item in siteUrl:
		temp = []
		temp.append(line[0])
		temp.append(line[1])
		temp.append(item)
		writer.writerow(temp)
csvRead.close()
csvWrite.close()
