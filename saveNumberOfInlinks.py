# Does the following
# 1) Calculates the a) number of inlinks b) number of outlinks for an input concept and stores result in a file.

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
		self.dict2 = {}
		self.dict3 = {}
		self.inputConcepts = []
		#self.concept1 = "Network security"
		#self.concept2 = "f"
		self.aNeedsB = 0
		self.bNeedsA = 0
		self.tempConcept = ""
		self.tempParent = ""
		self.possibleParent = ""
		self.queue=[]
		self.queue1=[]
		self.queue2=[]
		self.visited = []
		self.refdValues = []
		self.outputFiles = []
		
		self.f = open("/home/prajna/neo4j/input/inputConceptsToKnowLength")
		for line in self.f:
			line = line[:-1]
			self.inputConcepts.append(line.replace(" ","_").lower())
		for i in range(len(self.inputConcepts)):
			self.outputFiles.append("")
		output = "/home/prajna/neo4j/input/toposortTrees/inlinksInformation/inlinks"
		self.outputFiles = open(output,"w")
		#self.o = open("/home/prajna/neo4j/output/prerequisiteTreeLargeQOWithRefD","w")
		#self.o1 = open("RefDOrderManyConcepts","w")
	def startElement(self, name, attrs):
		self.count = self.count + 1
		if self.count % 1000000 == 0:
			print self.count
		if name == "p":
			self.pageFlag = True
		elif self.pageFlag:
			if name == "t":
				self.titleFlag = True
			elif name == "l":
				self.linkFlag = True
	def endElement(self,name):
		if name == "p":
			self.pageFlag = False
			self.titleName = ""
		if name == "t":
			self.titleFlag = False
		if name == "l":
			self.linkFlag = False
			self.linkName = ""
		if name == "d":
			for item in self.dict1.keys():
				self.dict3[item] = 0
				for elem in self.dict1[item]: 
					self.dict3[elem] = 0
			#implement BFS code here
			print len(self.dict1)
			print sys.getrecursionlimit
			for item in self.dict1.keys():
				for elem in self.dict1[item]:	
					self.dict3[elem] = self.dict3[elem] + 1
			
			counter = 0
			allConcepts = []
			for concept1 in self.inputConcepts:
				self.queue.append((concept1,0))
				self.queue2.append(concept1)
				self.queue1.append((concept1,0))
				
				while(len(self.queue)<>0):
					#print len(self.queue)
					a = self.queue.pop(0)
					b = self.queue2.pop(0)
					self.visited.append(a[0])
					
					if(a[1]==2):
						continue
					
					for item in self.dict1[a[0]]:
						#print item
						if(item not in self.queue2 and item not in self.visited):
							count = a[1]
							self.queue.append((item,count+1))
							self.queue1.append((item,count+1))
							self.queue2.append(item)
							#self.dict2[item]=a[0]
				for elem in self.queue1:
					allConcepts.append(elem[0])
				
							#self.dict3[item].append(a[0])
				self.queue1 = []
				self.queue2 = []
				self.queue = []
				self.dict2 = {}
				self.visited = []
				counter = counter + 1
			allConcepts = list(set(allConcepts))
			for item in allConcepts:
				self.outputFiles.write(str(item)+"\t"+str(self.dict3[item])+str(len(self.dict1[item]))+"\n")
				
	def characters(self, content):
		if (content<>"\n"):
			if self.titleFlag == True and self.linkFlag == False:
				self.titleName = content.replace(" ","_").lower().encode('utf-8')
				#print ("content: "+content)
				if(self.titleName not in self.dict1):
					self.dict1[self.titleName] = []
			elif self.titleFlag == False and self.linkFlag == True:
				self.linkName = content.replace(" ","_").lower().encode('utf-8')
				self.dict1[self.titleName].append(self.linkName)
				if self.linkName not in self.dict2:
					self.dict2[self.linkName] = []
					self.dict2[self.linkName].append(self.titleName)
				else:
					self.dict2[self.linkName].append(self.titleName)
				if(self.linkName not in self.dict1):
					self.dict1[self.linkName] = []
				if(self.titleName not in self.dict2):
					self.dict2[self.titleName] = []
					
	def referenceDistance(self):
		for i in self.dict1[self.tempConcept1]:
			if(self.tempConcept2 in self.dict1[i]):
				self.aNeedsB = self.aNeedsB + 1
		for i in self.dict1[self.tempConcept2]:
			if(self.tempConcept1 in self.dict1[i]):
				self.bNeedsA = self.bNeedsA + 1
		if (len(self.dict1[self.tempConcept2])<>0 and len(self.dict1[self.tempConcept1])<>0):
			self.refd = float(self.aNeedsB)/float(len(self.dict1[self.tempConcept1])) - float(self.bNeedsA)/float(len(self.dict1[self.tempConcept2]))			
			
		else:
			self.refd = -9999
		self.aNeedsB = 0
		self.bNeedsA = 0
	
	def isParent(self):
		if self.isParentFlag == True:
			return
		for parent in self.dict3[self.possibleParent]:
			if parent == self.tempParent:
				self.isParentFlag = True
				return
			else:
				self.possibleParent = parent
				self.isParent()

def main(sourceFileName):
	sys.setrecursionlimit(10000)
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
	start_time = time.time()
	main("/home/prajna/neo4j/input/newWikiLinks.xml")
	print time.time() - start_time
	


