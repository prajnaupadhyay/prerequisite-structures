#filters the technical content out

import xml.sax
import time
import operator

class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.titleFlag = False
		self.uptoTitleFlag = False
		self.collectPage = False
		self.tagAndAttributes1 = []
		self.tagAndAttributes2 = []
		self.tagAndAttributes3 = []
		self.inputConcepts = []
		self.f = open("/home/pearl/fromOlivaw/neo4jbackup/input/smallInputConceptsToKnowLength")
		self.o = open("/home/pearl/fromOlivaw/neo4jbackup/output/recreatedXMLnew.xml","w")
		for line in self.f:
			line = line[:-1]
			self.inputConcepts.append(line)
		
	def startElement(self, name, attrs):
		if name == "page":
			self.uptoTitleFlag = True
			self.tagAndAttributes1.append(name)
			self.tagAndAttributes2.append(attrs)
			self.tagAndAttributes3.append("")
		elif name == "title":
			self.tagAndAttributes1.append(name)
			self.tagAndAttributes2.append(attrs)
			self.tagAndAttributes3.append("")
			self.titleFlag = True
			self.uptoTitleFlag = False
		if self.collectPage == True:
			self.o.write("<"+name)
			print name
			for key in attrs.keys():
				self.o.write(" "+str(key)+" = "+'"'+str(attrs[key])+'"')
			self.o.write(">")
		elif self.uptoTitleFlag == True:
			self.tagAndAttributes1.append(name)
			self.tagAndAttributes2.append(attrs)
			self.tagAndAttributes3.append("")
		
	def endElement(self,name):
		if self.collectPage == True:
			self.o.write("</"+name+">")
		elif name == "title":
			self.titleFlag = False
		
	def characters(self, content):
		if self.titleFlag == True and content in self.inputConcepts:
			self.tagAndAttributes3[len(self.tagAndAttributes3)-1] = content
			for i in range(len(self.tagAndAttributes1)):
				self.o.write("<"+self.tagAndAttributes1[i])
				for key in self.tagAndAttributes2[i].keys():
					self.o.write(" "+str(key)+" = "+'"'+str(self.tagAndAttributes2[i][key])+'"')
				self.o.write(">")
				self.o.write(str(self.tagAndAttributes3[i]))
				self.o.write("</"+str(self.tagAndAttributes1[i])+">")
				self.collectPage = True
		elif self.uptoTitleFlag == True:
			self.tagAndAttributes3[len(self.tagAndAttributes3)-1] = content
		elif self.collectPage == True:
			self.o.write(str(content.encode("utf-8")))
			
		
def main(sourceFileName):
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
	start_time = time.time()
	main("/home/pearl/fromOlivaw/neo4jbackup/input/sample_page.xml")
	print time.time() - start_time
	
