import sys
import os
from os import listdir
from os.path import isfile, join
from operator import itemgetter
import operator

def findLevel(dictChild, node):
	#print node
	if len(dictChild[node])==0:
		return 0
	listLevel = []
	for item in dictChild[node]:
		listLevel.append(findLevel(dictChild, item))
	return max(listLevel) + 1

def createTreeAndOtherEdges(f, newDirPath, mypath):
	print f
	f1 = open(mypath+f)
	#o1 = open(newDirPath+f+"_treeEdges","w")
	o2 = open(newDirPath+f+"_onlyBackEdges","w")
	index = f[:f.rfind("_")].rfind("_")
	inputConcept = f[index+1:]
	dict1 = {}
	dictChild = {}
	dictLevel = {}
	for line in f1:
		line = line[:-1]
		splitline = line.split("\t")
		if splitline[0] not in dict1.keys():
			dict1[splitline[0]] = []
			dict1[splitline[0]].append(splitline[1])
		else:
			dict1[splitline[0]].append(splitline[1])
		if splitline[1] not in dict1.keys():
			dict1[splitline[1]] = []
	
	if len(dict1.keys()) == 0:
		return
		
	order = []

	queue = []
	queue1 = []
	queue2 = []
	visited = []
	otherEdges = []
	dict2 = {}
	for item in dict1.keys():
		dict2[item] = ""

	queue.append(inputConcept)
	queue1.append((inputConcept,0))
	queue2.append((inputConcept,0))
	while (len(queue)<>0):
		a = queue1.pop(0)
		b = queue.pop(0)
		visited.append(a[0])
		for item in dict1[a[0]]:
			if item not in visited and item not in queue:
				level = a[1]
				dict2[item] = a[0]
				if a[0] not in dictChild:
					dictChild[a[0]] = []
					dictChild[a[0]].append(item)
				else:
					dictChild[a[0]].append(item)
				if item not in dictChild:
					dictChild[item] = []
				queue.append(item)
				queue1.append((item,level+1))
				queue2.append((item,level+1))
			#else:
				#otherEdges.append((a[0],item))
			elif item in visited:
			#print item+"visited twice"
			#print a[0]+"visited from"
				newItem = a[0]
				flag = False
				while(dict2[newItem]<>item):
					if dict2[newItem]<>"":
						newItem = dict2[newItem]
					else:
						flag = True
						break
				#print flag
				if flag == False:
					print flag
					otherEdges.append((a[0],item))
	'''			
	for item in dict2.keys():
		dictChild[dict2[item]].append(item)
	
	
	for item in dict1.keys():
		#print item
		dictLevel[item] = findLevel(dictChild, item)
		
	sortedDictLevel = sorted(dictLevel.items(),key=operator.itemgetter(1))
				
	for item in reversed(sortedDictLevel):
		if item[0] in dict2:
			o1.write(dict2[item[0]]+"\t"+item[0]+"\n")
	'''
	for item in otherEdges:
		o2.write(item[0]+"\t"+item[1]+"\n")
	
	f1.close()
	#o1.close()
	o2.close()

dict1 = {}
mypath1 = sys.argv[1]
onlyfiles1 = [f for f in listdir(mypath1) if isfile(join(mypath1, f))]

mypath2 = sys.argv[2]
onlyfiles2 = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]

mypath3 = sys.argv[3]
onlyfiles3 = [f for f in listdir(mypath3) if isfile(join(mypath3, f))]

for f in onlyfiles1:
	newDirPath = mypath1+"onlyBackEdges/"
	if not os.path.exists(newDirPath):
		os.makedirs(newDirPath)
	#f1 = open(mypath1+f)
	createTreeAndOtherEdges(f, newDirPath, mypath1) 

for f in onlyfiles2:
	newDirPath = mypath2+"onlyBackEdges/"
	if not os.path.exists(newDirPath):
		os.makedirs(newDirPath)
	#f1 = open(mypath2+f)
	createTreeAndOtherEdges(f, newDirPath, mypath2) 

for f in onlyfiles3:
	newDirPath = mypath3+"onlyBackEdges/"
	if not os.path.exists(newDirPath):
		os.makedirs(newDirPath)
	#f1 = open(mypath3+f)
	createTreeAndOtherEdges(f, newDirPath, mypath3) 


