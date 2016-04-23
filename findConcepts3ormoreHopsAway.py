#Does the following
# 1) Collect all the concepts located at 3 hop distance away from the input concept to see if they are at all prerequisites


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
		self.queue2=[]
		self.visited = []
		self.refdValues = []
		self.f = open("/home/prajna/neo4j/input/singleInput")
		for line in self.f:
			line = line[:-1]
			self.inputConcepts.append(line.replace(" ","_").lower())
		self.o = open("/home/prajna/neo4j/output/3hopConceptsSGT","w")
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
				self.queue.append((concept1,0))
				self.queue1.append((concept1,0))
				self.visited.append(concept1)
				while(len(self.queue)<>0):
					a = self.queue.pop(0)
					if(a[1]==3):
						self.queue2.append((a[0],3))
						continue
					for item in self.dict1[a[0]]:
						if(item not in self.visited):
							count = a[1]
							self.visited.append(item)
							self.queue.append((item,count+1))
							self.queue1.append((item,count+1))
				
				self.o.write("\n"+concept1+"#######\n\n")
				'''
				self.tempConcept1 = concept1
				
				for item in reversed(self.queue1):
					self.tempConcept2 = item[0]
					self.referenceDistance()
					self.refdValues.append((self.tempConcept2,self.refd))
				self.refdValues.sort(key=operator.itemgetter(1))
				'''
				self.queue = []
				self.queue1 = []
				self.visited = []
				
				
				for item in self.queue2:
					self.o.write(str(item)+"\n")
				'''
				for val in reversed(self.refdValues):
					self.o.write("\n"+str(val)+"\n")
				
				for i in range((len(self.refdValues)-1),0,-1):
					if(self.refdValues[i][1]>0.0):
						self.tempConcept1 = self.refdValues[i][0]
						for j in range(i-1,-1,-1):
							self.tempConcept2 = self.refdValues[j][0]
							self.referenceDistance()
							if(self.refd>0.0):
								self.o.write("Reference distance between "+self.tempConcept1.encode("utf-8")+" and "+self.tempConcept2.encode("utf-8")+" is:"+str(self.refd)+"\n")
				'''
				self.refdValues = []
				self.queue2 = []
											
						
			
			'''
			for c in self.dict1:
				print c
			
			for c in self.dict1[self.concept1]:
				if(self.concept2 in self.dict1[c]):
					self.aNeedsB = self.aNeedsB + 1
			#self.aNeedsB = self.aNeedsB / len(self.dict1[self.concept1])
			for c in self.dict1[self.concept2]:
				if(self.concept1 in self.dict1[c]):
					self.bNeedsA = self.bNeedsA + 1
			#self.bNeedsA = self.bNeedsA / len(self.dict1[self.concept2])
			
			print self.aNeedsB
			print len(self.dict1[self.concept1])
			print self.bNeedsA
			print len(self.dict1[self.concept2])
			'''
			
			#print (float(self.aNeedsB)/float(len(self.dict1[self.concept1])) - float(self.bNeedsA)/float(len(self.dict1[self.concept2])))
			
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
	main("/home/prajna/neo4j/input/newWikiLinks.xml")
	print time.time() - start_time
	

