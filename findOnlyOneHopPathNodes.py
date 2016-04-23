#Does the following
# 1) Collect all the concepts located at most 2 hop distance away from the input concept 
# 2) Find out RefD score for each of them and sort them in decreasing order
# 3) Find out pairs for an input concept which are contradictory
# 4) Incomplete

import xml.sax
import time
import operator

class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.count = 0
		self.pageFlag = False
		self.titleFlag = False
		self.titleName = ""
		self.linkFlag = False
		self.linkName = ""
		self.dict1 = {}
		self.inputConcepts = []
		#self.concept1 = "Network security"
		#self.concept2 = "f"
		self.aNeedsB = 0
		self.bNeedsA = 0
		self.tempConcept = ""
		self.queue=[]
		self.queue1=[]
		self.visited = []
		self.refdValues = []
		self.f = open("/home/pearl/fromOlivaw/neo4jbackup/input/inputConceptsToKnowLength1")
		for line in self.f:
			line = line[:-1]
			self.inputConcepts.append(line.replace(" ","_").lower())
		self.o = open("/home/pearl/fromOlivaw/neo4jbackup/output/conceptAndCount1","w")
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
			#implement BFS code here
			print len(self.dict1)
			
			for concept1 in self.inputConcepts:
				neighboursOfNeighbours = []
				leftOverElements = []
				for item in self.dict1[concept1]:
					neighboursOfNeighbours.extend(self.dict1[item])
				leftOverElements = list(set(self.dict1[concept1]) - set(neighboursOfNeighbours))
				
				self.o.write("\n"+concept1+"#######\t"+str(float(len(leftOverElements))/float(len(self.dict1[concept1])))+"\n\n")
				for item in leftOverElements:
					self.o.write(str(item.encode('utf-8'))+"\n")
				
	def characters(self, content):
		if (content<>"\n"):
			if self.titleFlag == True and self.linkFlag == False:
				self.titleName = content.replace(" ","_").lower()
				#print ("content: "+content)
				if(self.titleName not in self.dict1):
					self.dict1[self.titleName] = []
			elif self.titleFlag == False and self.linkFlag == True:
				self.linkName = content.replace(" ","_").lower()
				self.dict1[self.titleName].append(self.linkName)
				if(self.linkName not in self.dict1):
					self.dict1[self.linkName] = []
					
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

def main(sourceFileName):
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
	start_time = time.time()
	main("/home/pearl/fromOlivaw/neo4jbackup/input/newWikiLinks.xml")
	print time.time() - start_time
	

