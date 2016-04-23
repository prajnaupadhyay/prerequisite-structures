#Fiters the techincal content out from the output returned from dizzy logic parser

import xml.sax
import time
import operator

class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.titleFlag = False
		self.firstPara = False
		self.target = False
		self.collectPage = False
		self.doubleContent = False
		self.fileFlag = False
		self.count = 0
		self.inputConcepts = []
		self.f = open("/home/pearl/fromOlivaw/neo4jbackup/input/conceptsFromSeeds")
		self.o = open("/home/pearl/fromOlivaw/neo4jbackup/output/filteredPages.xml","w")
		#print "hi"
		for line in self.f:
			line = line[:-1]
			self.inputConcepts.append(line.replace(" ","_").lower())
		
	def startElement(self, name, attrs):
		if self.count == 0:
			self.o.write("<?xml version='1.0' encoding='UTF-8'?>\n<d>")
		self.count = self.count + 1
		if(self.count % 10000000) == 0:
			print self.count
		if name == "title":
			self.titleFlag = True
		elif name == "firstPara":
			self.firstPara = True
		elif name == "target":
			self.target = True
		
	def endElement(self,name):
		if name == "title" and self.titleFlag == True and self.collectPage == True: 
			self.titleFlag = False
			self.o.write("</t>\n")
		elif name == "firstPara" and self.firstPara == True and self.collectPage == True:
			self.firstPara = False
		elif self.collectPage == True and self.firstPara == True and self.target == True and name=="target":
			#print self.doubleContent
			if(self.fileFlag == False):
				self.target = False
				self.doubleContent = False
				self.o.write("</l>\n")
			else:
				self.fileFlag = False
				self.target = False
				self.doubleContent = False
		elif name == "page" and self.collectPage == True:
			self.collectPage = False
			self.o.write("</p>\n")
		
	def characters(self, content):
		if self.titleFlag == True and content.replace(" ","_").lower().encode('utf-8') in self.inputConcepts:
			self.o.write("<p>\n")
			self.o.write("<t>"+str(content.encode('utf-8')))
			self.collectPage = True
		elif self.collectPage == True and self.firstPara == True and self.target == True:
			#print content
			#print self.doubleContent
			if(self.doubleContent == False):
				if(len(content)>5):
					#print content
					if(content[:5]!="File:"):
						
						self.o.write("<l>"+str(content.encode("utf-8")))
						self.doubleContent = True
					else:
						#print "file found"
						self.fileFlag = True
						self.doubleContent = True
				else:
					self.o.write("<l>"+str(content.encode("utf-8")))
					self.doubleContent = True
			elif self.doubleContent == True:
				if(len(content)>5):
					#print content
					if(content[:5]!="File:"):
						self.o.write(str(content.encode("utf-8")))
						self.doubleContent = True
					else:
						#print "file found"
						self.fileFlag = True
				else:
					self.o.write(str(content.encode("utf-8")))
					self.doubleContent = True
				
#print content.encode("utf-8")
			
		
def main(sourceFileName):
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())
	ao = open("/home/pearl/fromOlivaw/neo4jbackup/output/recreatedPandLXML.xml","a")
	ao.write("</d>")
	ao.close()
 
if __name__ == "__main__":
	start_time = time.time()
	main("/home/pearl/fromOlivaw/neo4jbackup/input/articles_in_xml.xml")
	
	print time.time() - start_time
	
