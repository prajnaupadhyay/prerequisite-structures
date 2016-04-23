#incomplete

import re
import operator

def findLevel(childTree, node):
	if len(childTree[node])==0:
		return 0
	listLevel = []
	for item in childTree[node]:
		listLevel.append(findLevel(childTree, item))
	return max(listLevel) + 1
	
def pruneNodes(snakeCaseItem, item, dictTree, dictChild, d1, thresh):
	if item[0]==snakeCaseItem:
		return
	if d1[snakeCaseItem][item[0]] < thresh:
		if len(dictChild[item[0]])>0:
			for elem in dictChild[item[0]]:
				dictTree[elem] = dictTree[item[0]]
				dictChild[dictTree[item[0]]].append(elem)
				if item[0] in dictChild[dictTree[item[0]]]:
					dictChild[dictTree[item[0]]].remove(item[0])
				dictChild[item[0]]=[]
			dictTree[item[0]]=""
		else:
			dictChild[dictTree[item[0]]].remove(item[0])
			dictTree[item[0]] = ""
			
def pruneNodesScope(snakeCaseItem, item, dictTree, dictChild, d1, thresh):
	if item[0]==snakeCaseItem:
		return
	if abs(d1[snakeCaseItem] - d1[item[0]]) > thresh:
		if len(dictChild[item[0]])>0:
			for elem in dictChild[item[0]]:
				dictTree[elem] = dictTree[item[0]]
				dictChild[dictTree[item[0]]].append(elem)
				if item[0] in dictChild[dictTree[item[0]]]:
					dictChild[dictTree[item[0]]].remove(item[0])
				dictChild[item[0]]=[]
			dictTree[item[0]]=""
		else:
			dictChild[dictTree[item[0]]].remove(item[0])
			dictTree[item[0]] = ""
					

	
def pruneTrees(snakeCaseItem, threshList, d, relevanceDict, scopelist, inlinksDict):
	dictTree = {}
	orgDictTree = {}
	dictChild = {}
	orgDictChild = {}
	dictLevel = {}
	
	filteredNodes = []
	
	f4 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/treeAndOtherEdges/"+snakeCaseItem+"_treeEdges")
	for line in f4:
		line = line[:-1]
		splitLine = line.split("\t")
		if splitLine[0] not in dictTree and splitLine[1] not in dictTree:
			dictTree[splitLine[0]] = ""
			dictTree[splitLine[1]] = splitLine[0]
		elif splitLine[1] not in dictTree and splitLine[0] in dictTree:
			dictTree[splitLine[1]] = splitLine[0]
		elif splitLine[0] not in dictTree and splitLine[1] not in dictTree:
			dictTree[splitLine[0]] = ""
		else:
			dictTree[splitLine[1]] = splitLine[0]
			
		if splitLine[0] not in dictChild and splitLine[1] not in dictChild:
			dictChild[splitLine[0]] = []
			dictChild[splitLine[1]] = []
			dictChild[splitLine[0]].append(splitLine[1])
		elif splitLine[1] not in dictChild and splitLine[0] in dictChild:
			dictChild[splitLine[0]].append(splitLine[1])
			dictChild[splitLine[1]] = []
		elif splitLine[0] not in dictChild and splitLine[1] in dictChild:
			dictChild[splitLine[0]] = []
			if splitLine[1] not in dictChild[splitLine[0]]:
				dictChild[splitLine[0]].append(splitLine[1])
		else:
			dictChild[splitLine[0]].append(splitLine[0])
		
	f4.close()
	print len(dictChild)
	print len(dictTree)
	
	'''
	#print len(list(set(orgKeys)))
	f4 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/treeAndOtherEdges/"+snakeCaseItem+"_treeEdges")	
	for line in f4:
		line = line[:-1]
		splitLine = line.split("\t")
		dictTree[splitLine[1]] = splitLine[0]
		dictChild[splitLine[0]].append(splitLine[1])
	'''
	allKeys = list((set(dictTree.keys()) | set(dictChild.keys())))
	
	filteredNodes = set(allKeys)
	
	orgDictTree = dictTree
	orgdDictChild = dictChild
	
	for item in filteredNodes:
		dictLevel[item] = 0
	for item in filteredNodes:
		dictLevel[item] = findLevel(dictChild, item)
		#print item+"\t"+dictLevel[item]
		
	sortedDictLevel = sorted(dictLevel.items(),key=operator.itemgetter(1))
	
	
	for item in sortedDictLevel:
		if item[0]==snakeCaseItem:
			continue
		if item[0] not in d[snakeCaseItem]:
			print "not present, so the tree should be pruned"
			if len(dictChild[item[0]])>0:
				"not present, so the tree should be pruned and has at least one child"
				for elem in dictChild[item[0]]:
					dictTree[elem] = dictTree[item[0]]
					dictChild[dictTree[item[0]]].append(elem)
					if item[0] in dictChild[dictTree[item[0]]]:
						dictChild[dictTree[item[0]]].remove(item[0])
					dictChild[item[0]]=[]
				dictTree[item[0]]=""
			else:
				dictChild[dictTree[item[0]]].remove(item[0])
				dictTree[item[0]] = ""
				
	print len(dictTree)
	print len(dictChild)
			
	
	for thresh in threshList:
		o = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/treeAndOtherEdges/prunedOnRefD/"+snakeCaseItem+"_"+str(thresh),"w")
		
		for item in sortedDictLevel:
			pruneNodes(snakeCaseItem, item, dictTree, dictChild, d, thresh)
			
		for item in reversed(sortedDictLevel):
			if len(dictChild[item[0]])>0:
				for elem in dictChild[item[0]]:
					o.write(item[0]+"\t"+elem+"\n")
		o.close()
	
	dictChild = orgDictChild
	dictTree = orgDictTree
	
	for thresh in threshList:
		o = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/treeAndOtherEdges/prunedOnRelevance/"+snakeCaseItem+"_"+str(thresh),"w")
		
		for item in sortedDictLevel:
			pruneNodes(snakeCaseItem, item, dictTree, dictChild, relevanceDict, thresh)
			
		for item in reversed(sortedDictLevel):
			if len(dictChild[item[0]])>0:
				for elem in dictChild[item[0]]:
					o.write(item[0]+"\t"+elem+"\n")
		o.close()
	
	
	dictChild = orgDictChild
	dictTree = orgDictTree
	
	for scope in scopelist:
		o = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/treeAndOtherEdges/prunedOnScope/"+snakeCaseItem+"_"+str(scope),"w")
		
		for item in sortedDictLevel:
			pruneNodesScope(snakeCaseItem, item, dictTree, dictChild, inlinksDict, scope)
			
		for item in reversed(sortedDictLevel):
			if len(dictChild[item[0]])>0:
				for elem in dictChild[item[0]]:
					o.write(item[0]+"\t"+elem+"\n")
		o.close()

	f4.close()
	

inputConcepts = ["concurrencyControl","foreignKey","functionalDependency","queryOptimization","queryPlan","referentialIntegrity","scapegoatTree"]


#inputConcepts = ["concurrencyControl"]
threshList = [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
scopelist = [10, 20, 30, 40, 50]
d = {}
inlinksDict = {}
relevanceDict = {}
#threshList = [0.0]
for concept in inputConcepts:
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', concept)
	inputConcept = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
	f1 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+inputConcept)
	for line in f1:
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
f2 = open("/home/prajna/neo4j/scripts/latestTreesScripts/output/relevance1")
f3 = open("/home/prajna/neo4j/input/toposortTrees/inlinksInformation/inlinks")
for line in f2:
	line = line[:-1]
	splitline = line.split("\t")
	if splitline[0] in relevanceDict and splitline[1] in relevanceDict:
		relevanceDict[splitline[0]][splitline[1]] = float(splitline[2])
		relevanceDict[splitline[1]][splitline[0]] = float(splitline[2])
	elif splitline[1] in relevanceDict and splitline[0] not in relevanceDict:
		relevanceDict[splitline[0]] = {}
		relevanceDict[splitline[0]][splitline[1]] = float(splitline[2])
		relevanceDict[splitline[1]][splitline[0]] = float(splitline[2])
	elif splitline[0] in relevanceDict and splitline[1] not in relevanceDict:
		relevanceDict[splitline[1]] = {}
		relevanceDict[splitline[0]][splitline[1]] = float(splitline[2])
		relevanceDict[splitline[1]][splitline[0]] = float(splitline[2])
	else:
		relevanceDict[splitline[1]] = {}
		relevanceDict[splitline[0]] = {}
		relevanceDict[splitline[0]][splitline[1]] = float(splitline[2])
		relevanceDict[splitline[1]][splitline[0]] = float(splitline[2])



for line in f3:
	line = line[:-1]
	splitline = line.split("\t")
	inlinksDict[splitline[0]] = int(splitline[1])
	
print "loaded the dictionaries"

for concept in inputConcepts:
	print concept
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', concept)
	snakeCaseItem = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
	
	pruneTrees(snakeCaseItem, threshList, d, relevanceDict, scopelist, inlinksDict)
	
f1.close()
f2.close()
f3.close()
	

