#coding:utf-8
import urllib2
import lxml
import csv
from lxml import *
import lxml.html
from urllib2 import HTTPError
import codecs



def main():
	csvRead = file('tieba1.csv','rb')
	reader = csv.reader(csvRead)

	csvWrite = open('result.csv',"wb")
	csvWrite.write(codecs.BOM_UTF8)
	writer = csv.writer(csvWrite,quoting=csv.QUOTE_ALL)

	for line in reader:
		try:
			html = urllib2.urlopen(line[1]).read()
			doc = lxml.html.document_fromstring(html)
			title = doc.xpath("/html/head/title/text()")
			print "url = "+line[1]+"'s title is "+ title[0]
			l = [line[0],line[1],title[0].encode('utf-8')]
			writer.writerow(l)
		except Exception, e:
			print e
	csvRead.close()
	csvWrite.close()

if __name__ == '__main__':
	main()

