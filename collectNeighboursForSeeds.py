# Does the following
# 1) Collects the neighbours for a concept located upto 2 hops away from a seed input concept. Input is a list of seed concepts

import xml.sax
import time
import operator
import networkx as nx
import matplotlib.pyplot as plt

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
		self.f = open("/home/pearl/fromOlivaw/neo4jbackup/input/seedList")
		for line in self.f:
			line = line[:-1]
			self.inputConcepts.append(line.replace(" ","_").lower())
		self.o = open("/home/pearl/fromOlivaw/neo4jbackup/output/conceptsFromSeeds","w")
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
			for key in self.dict1:
				self.dict2[key]=""
			
			for concept1 in self.inputConcepts:
				self.queue.append((concept1,0))
				self.queue2.append(concept1)
				self.queue1.append(concept1)
				
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
							self.queue1.append(item)
							self.queue2.append(item)
							self.dict2[item]=a[0]
				self.queue = []
				self.queue2 = []
			
			self.queue1 = list(set(self.queue1))
			self.queue1.sort()
			for item in self.queue1:
				self.o.write(str(item.encode('utf-8'))+"\n")
				'''
				G=nx.DiGraph()
				for item in self.queue1:
					G.add_node(str(item[0]))
				for item in graph:
					G.add_edge(item[0],item[1])
				pos = nx.spring_layout(G)
				
				for item in nodes:
					labels[item]=item
				
				nx.write_dot(G,'test.dot')
				#labels["a"]="a"
				nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_color='r',node_size=500,alpha=0.8)
				nx.draw_networkx_labels(G,pos,labels,font_size=12)
				nx.draw_networkx_edges(G,pos,edgelist=graph,width=2,alpha=0.5,edge_color='b')
				#nx.draw_networkx_labels(G,pos,labels)
				plt.show()
				'''
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
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
	start_time = time.time()
	main("/home/pearl/fromOlivaw/neo4jbackup/input/newWikiLinks.xml")
	print time.time() - start_time
	


