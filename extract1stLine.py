import xml.sax
import time
import operator
import networkx as nx
import matplotlib.pyplot as plt
import sys

class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.count = 0
		self.pageFlag = False
		self.titleFlag = False
		self.isParentFlag = False
		self.titleName = ""
		self.linkFlag = False
		self.linkName = ""
		self.dict1 = {}
		self.conceptList = []
		self.o = open("/home/prajna/neo4j/scripts/latestTreesScripts/output/firstLineForConcepts","w")
		self.f = open("/home/prajna/neo4j/scripts/latestTreesScripts/prunedConceptList")
		for line in self.f:
			line = line[:-1]
			self.conceptList.append(line)
	
	def startElement(self, name, attrs):
		self.count = self.count + 1
		if self.count % 1000000 == 0:
			print self.count
		if name == "doc":
			self.pageFlag = True
		elif self.pageFlag:
			if name == "title":
				self.titleFlag = True
			elif name == "abstract":
				self.linkFlag = True
	def endElement(self,name):
		if name == "doc":
			self.pageFlag = False
			self.titleName = ""
		if name == "title":
			self.titleFlag = False
		if name == "abstract":
			self.linkFlag = False
			self.linkName = ""
		if name == "feed":
			#implement BFS code here
			print len(self.dict1)
			#newList = set(self.dict1.keys()).intersection(self.conceptList)
			for item in self.dict1.keys():
				#self.o.write(str(item).encode('utf-8')+"\t"+str(self.dict1[item][0])+"\n")
				self.o.write(item.encode('utf-8'))
				self.o.write("\t")
				self.o.write(self.dict1[item].encode('utf-8'))
				self.o.write("\n")
				#print self.dict1[item]
				
	def characters(self, content):
		if (content<>"\n"):
			if self.titleFlag == True and self.linkFlag == False:
				self.titleName = content.replace("Wikipedia: ","").replace(" ","_").lower()
				if(self.titleName not in self.dict1):
					self.dict1[self.titleName] = ""
					
			elif self.titleFlag == False and self.linkFlag == True:
				self.linkName = content
				self.dict1[self.titleName] = self.linkName
				
					
def main(sourceFileName):
	sys.setrecursionlimit(10000)
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
	start_time = time.time()
	main("/home/prajna/wikipediajan2016dump/enwiki-latest-abstract.xml")
	print time.time() - start_time
