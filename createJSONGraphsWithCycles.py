#for a given directory, it converts all the files (containing trees) into JSON format 

from os import listdir
from os.path import isfile, join
import os
import json
import re
import sys 

def createJSONGraphs(mypath, f, d):
	newDirPath = mypath+"JSONFiles1/"
	if not os.path.exists(newDirPath):
		os.makedirs(newDirPath)
	f1 = open(mypath+f) 
	f3 = open("/home/prajna/neo4j/input/toposortTrees/inlinksInformation/inlinks")
	inlinksInformation = {}
	for line in f3:
		line = line[:-1]
		splitline = line.split("\t")
		inlinksInformation[splitline[0]] = int(splitline[1])
	o = open(newDirPath+f+"_intermediate.json","w")        
	data = []                                                                                                                                                                                              
	pattern = re.compile("[\W]*(\".*\"): \[")
	pattern1 = re.compile("[\W]*(\".*\"): \[\]")
	
	for line in f1:
		line = line[:-1]
		splitLine = line.split("\t")
		data.append((splitLine[0]+"_"+str(inlinksInformation[splitLine[0]]),splitLine[1]+"_"+str(inlinksInformation[splitLine[1]])))                                                                                                                                                                                        
	f1.close()
	if len(data) == 0:
		return
	root = data[0][0]
                                                                                                                                                                                        
	node2chilren = {root: []}                                                                                                                                                                                          
	for parent, child in data:                                                                                                                                                                                         
		childnode = {child: []}                                                                                                                                                                                        
		children = node2chilren[parent]                                                                                                                                                                                
		children.append(childnode)                                                                                                                                                                                     
		node2chilren[child] = childnode[child]                                                                                                                                                                         

	jsonstr = json.dumps({root: node2chilren[root]}, indent=1)                                                                                                                                                         
	o.write(jsonstr)
	o.close()
	f1 = open(newDirPath+f+"_intermediate.json")
	o = open(newDirPath+f+".json","w")
	for line in f1:
		line= line[:-1]
		#print line
		if pattern.match(line) is not None and pattern1.match(line) is None:
			p = pattern.match(line)
			newStr = '"name":'+p.group(1)+',"children": [\n'
			o.write(newStr)
		elif pattern1.match(line) is not None:
			#print "pattern1"
			p = pattern1.match(line)
			newStr = '"name":'+p.group(1)+',"children": []\n'
			o.write(newStr)
		else:
			o.write(line+"\n")
	o.write("}")
	o.close()

mypath = sys.argv[1]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
'''
inputConcepts = ["concurrency_control","foreign_key","referential_integrity","functional_dependency","scapegoat_tree","query_plan","query_optimization"]
d = {}
for inputConcept in inputConcepts:
	print "loading refdscore for "+inputConcept

	f2 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+inputConcept)

	for line in f2:
		line = line[:-1]
		splitline = line.split("\t")
		if splitline[0] in d and splitline[1] in d:
			#line = line[:-1]
			if splitline[2]<>'-9999':
				#print splitline[2]
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]][splitline[0]] = 0 - float(splitline[2])
			elif splitline[2]=='-9999':
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]][splitline[0]] = float(splitline[2])
		elif splitline[1] in d and splitline[0] not in d:
			if splitline[2]<>'-9999':
				d[splitline[1]][splitline[0]] = float(splitline[2])
				d[splitline[0]]={}
				d[splitline[0]][splitline[1]] = 0 - float(splitline[2])
			elif splitline[2]=='-9999':
				d[splitline[1]][splitline[0]] = float(splitline[2])
				d[splitline[0]]={}
				d[splitline[0]][splitline[1]] = float(splitline[2])
		elif splitline[0] in d and splitline[1] not in d:
			if splitline[2]<>'-9999':
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]]={}
				d[splitline[1]][splitline[0]] = 0 - float(splitline[2])
			elif splitline[2]=='-9999':
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]]={}
				d[splitline[1]][splitline[0]] = float(splitline[2])
		else:
			d[splitline[0]]={}
			d[splitline[1]]={}
			if splitline[2]<>'-9999':
				#print splitline[2]
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]][splitline[0]] = 0 - float(splitline[2])
			elif splitline[2]=='-9999':
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]][splitline[0]] = float(splitline[2])
	f2.close()
'''
d = {}
for f in onlyfiles:
	pattern = re.compile(".*_treeEdges")
	if pattern.match(f) is not None:
		print f
		createJSONGraphs(mypath, f, d)
	
	
