import sys
import os
from os import listdir
from os.path import isfile, join
from operator import itemgetter


def bfs(dict3, inputConcept, o):
	order = []
	queue = []
	queue1 = []
	queue2 = []
	visited = []
	queue.append(inputConcept)
	queue1.append((inputConcept,0))
	queue2.append((inputConcept,0))
	while (len(queue)<>0):
		a = queue1.pop(0)
		b = queue.pop(0)
		#print a
		visited.append(a[0])
		for item in dict3[a[0]]:
			if item not in visited and item not in queue:
				level = a[1]
				queue.append(item)
				queue1.append((item,level+1))
				queue2.append((item,level+1))
	queue2 = sorted(queue2, key=itemgetter(1))
	for item in reversed(queue2):
		o.write(str(item)+"\n")
		
mypath = sys.argv[1]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

inputConcepts = ["concurrency_control","foreign_key","referential_integrity","functional_dependency","scapegoat_tree","query_plan","query_optimization"]
d = {}
for inputConcept in inputConcepts:
	print "loading refdscore for "+inputConcept
	'''
	f2 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+inputConcept)
	for line in f2:
		line = line[:-1]
		splitLine = line.split("\t")
		d[splitLine[0]]={}
		d[splitLine[1]]={}
		d[splitLine[0]][splitLine[1]] = 0.0
		d[splitLine[1]][splitLine[0]] = 0.0
	f2.close()
	'''
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

for f in onlyfiles:
	dict1 = {}
	dict2 = {}
	#d = {}
	index = f[:f.rfind("_")].rfind("_")
	inputConcept = f[index+1:]
	print f+"\t"+inputConcept
	newDirPath = mypath+"ReadingOrder/"
	if not os.path.exists(newDirPath):
		os.makedirs(newDirPath)
	f1 = open(mypath+f) 
	'''
	f2 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+inputConcept)
	
	d = {}
	for line in f2:
		line = line[:-1]
		splitLine = line.split("\t")
		d[splitLine[0]]={}
		d[splitLine[1]]={}
		d[splitLine[0]][splitLine[1]] = 0.0
		d[splitLine[1]][splitLine[0]] = 0.0
	f2.close()
	f2 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+inputConcept)
	
	for line in f2:
		line = line[:-1]
		splitline = line.split("\t")
		if splitline[0] in d:
			#line = line[:-1]
			if splitline[2]<>'-9999':
				#print splitline[2]
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]][splitline[0]] = 0 - float(splitline[2])
			elif splitline[2]=='-9999':
				d[splitline[0]][splitline[1]] = float(splitline[2])
				d[splitline[1]][splitline[0]] = float(splitline[2])
		elif splitline[1] in d:
			if splitline[2]<>'-9999':
				d[splitline[1]][splitline[0]] = float(splitline[2])
				d[splitline[0]][splitline[1]] = 0 - float(splitline[2])
			elif splitline[2]=='-9999':
				d[splitline[1]][splitline[0]] = float(splitline[2])
				d[splitline[0]][splitline[1]] = float(splitline[2])
	'''
	o = open(newDirPath+f,"w")
	for line in f1:
		line = line[:-1]
		splitline = line.split("\t")
		if splitline[0] == splitline[1]:
			continue
		if splitline[0] not in dict1.keys():
			dict1[splitline[0]] = []
		else:
			dict1[splitline[0]].append(splitline[1])
		if splitline[1] not in dict1.keys():
			dict1[splitline[1]] = []
		if splitline[0] not in dict2.keys():
			dict2[splitline[0]] = ""
		if splitline[1] not in dict2.keys():
			dict2[splitline[1]] = ""
	if len(dict1.keys())==0:
		o.write("no nodes")
		o.close()
		continue
			
	f1.close()
	newDict1 = {}
	newList = []
	#f1 = open(mypath+f)
	newList= set(dict1.keys()).intersection(d.keys())
	for item in newList:
		newDict1[item] = []
	for item in newList:
		newDict1[item] = set(dict1[item]).intersection(d.keys())
	'''
	print "before intersection dict1 keys"
	for item in dict1.keys():
		print item
	'''	
	dict1 = newDict1
	'''
	print "after intersection dict1 keys"
	
	for item in dict1.keys():
		print item
	'''		
	order = []

	queue = []
	queue1 = []
	queue2 = []
	visited = []
	
	queue.append(inputConcept)
	queue1.append((inputConcept,0))
	queue2.append((inputConcept,0))
	while (len(queue)<>0):
		a = queue1.pop(0)
		b = queue.pop(0)
		#print a
		visited.append(a[0])
		for item in dict1[a[0]]:
			if item not in visited and item not in queue:
				level = a[1]
				dict2[item] = a[0]
				queue.append(item)
				queue1.append((item,level+1))
				queue2.append((item,level+1))
			elif item in visited:
				#print item+"visited twice"
				#print a[0]+"visited from"
				edgeWeights = []
				newItem = a[0]
				flag = False
				while(dict2[newItem]<>item):
					if dict2[newItem]<>"":
						print newItem
						print dict2[newItem]
						#if dict2[newItem] not in d.keys():
							
						print d[dict2[newItem]][newItem]
						edgeWeights.append((dict2[newItem], newItem, d[dict2[newItem]][newItem]))
						
						newItem = dict2[newItem]
					else:
						flag = True
						break
				#print flag
				if flag == False:
					#print item
					if len(edgeWeights)==0:
						#print "two path cycle"
						edgeWeights.append((item, newItem, d[item][newItem]))
						edgeWeights.append((newItem, item, d[newItem][item]))
					elif len(edgeWeights)>0:
						edgeWeights.append((item, newItem, d[item][newItem]))
					edgeWeights = sorted(edgeWeights, key=itemgetter(2))
					elem = ""
					for elem in edgeWeights:
						#print elem
						if elem[0]<>inputConcept:
							break
					edgeWeights.remove(elem)
					dict2[elem[1]] = ""
					#edgeWeights = edgeWeights[1:]
						
					for elem in edgeWeights:
						dict2[elem[1]] = elem[0]
	dict3 = {}
	for item in dict2.keys():
		dict3[dict2[item]] = []
		dict3[item] = []
	for item in dict2.keys():
		dict3[dict2[item]].append(item)
	bfs(dict3, inputConcept,o)
	'''
	for key in dict2.keys():
		if dict2[key]<>"" and key<>inputConcept:
			o.write(dict2[key]+"\t"+key+"\n")
	'''
	o.close()
	f2.close()
	f1.close()
	
					
						
					
		  
