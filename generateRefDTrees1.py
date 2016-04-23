#generates the refd tree for an input concept

import operator
def createRefDTree(concept, d, n):
	preqTree = {}
	for key in d.keys():
		preqTree[key] = []
	refdTreeNodes = []
	refdTreeNodesOnly = []
	refdScores = []
	#print "concept"+concept
	refdTreeNodes.append((concept,1))
	e = 0
	flag = False
	for item in refdTreeNodes:
		#print item
		level = item[1]
		if e >= n:
			break
		else:
			refdScores = selectTopK(item[0], d)
			for item1 in refdScores:
				if item1[0] not in refdTreeNodesOnly:
					refdTreeNodes.append((item1[0],level+1))
					refdTreeNodesOnly.append(item1[0])
					#print "appending nodes to prerequisite tree"
				if(item[0] not in preqTree[item1[0]] and e<n):
					preqTree[item1[0]].append(item[0])
					e = e + 1
				elif e>=n:
					flag = True
					break
			if flag == True:
				break
	flag = False
	return preqTree
	
def createRefDTreeLevelWise(concept, d, n):
	preqTree = {}
	for key in d.keys():
		preqTree[key] = []
	refdTreeNodes = []
	refdTreeNodesOnly = []
	refdScores = []
	#print "concept"+concept
	refdTreeNodes.append((concept,0))
	for item in refdTreeNodes:
		#print item
		level = item[1]
		if level>=2:
			break
		else:
			refdScores = selectTopK(item[0], d, n)
			for item1 in refdScores:
				if item1[0] not in refdTreeNodesOnly:
					refdTreeNodes.append((item1[0],level+1))
					refdTreeNodesOnly.append(item1[0])
					#print "appending nodes to prerequisite tree"
				if(item[0] not in preqTree[item1[0]]):
					preqTree[item1[0]].append(item[0])
					
	return preqTree

def createRefDTreeWithThreshold(concept, d, n):
	preqTree = {}
	for key in d.keys():
		preqTree[key] = []
	refdTreeNodes = []
	refdTreeNodesOnly = []
	refdScores = []
	refdTreeNodes.append((concept,0))
	for item in refdTreeNodes:
		level = item[1]
		if level>=2:
			break
		else:
			refdScores = selectThresholdNodes(item[0], d, n)
			if len(refdScores) == 0:
				break
			else:
				for item1 in refdScores:
					if item1[0] not in refdTreeNodesOnly:
						refdTreeNodes.append((item1[0],level+1))
						refdTreeNodesOnly.append(item1[0])
						#print "appending nodes to prerequisite tree"
					if(item[0] not in preqTree[item1[0]]):
						preqTree[item1[0]].append(item[0])
					
	return preqTree
	
def createRefDTreeWithThresholdAndTopk(concept, d, n):
	preqTree = {}
	for key in d.keys():
		preqTree[key] = []
	refdTreeNodes = []
	refdTreeNodesOnly = []
	refdScores = []
	refdTreeNodes.append((concept,0))
	for item in refdTreeNodes:
		level = item[1]
		if level>=2:
			break
		else:
			refdScores = selectThresholdNodes(item[0], d, n)
			d1 = {}
			d1[item[0]] = {}
			for elem in refdScores:
				d1[item[0]][elem[0]] = elem[1]
			topk = 5
			refdScores = selectTopK(item[0], d1, topk)
			if len(refdScores) == 0:
				break
			else:
				for item1 in refdScores:
					if item1[0] not in refdTreeNodesOnly:
						refdTreeNodes.append((item1[0],level+1))
						refdTreeNodesOnly.append(item1[0])
						#print "appending nodes to prerequisite tree"
					if(item[0] not in preqTree[item1[0]]):
						preqTree[item1[0]].append(item[0])
					
	return preqTree


def selectTopK(concept, d, n):
	refdScores = []
	refdScores = sorted(d[concept].items(),key = operator.itemgetter(1))
	refdScores = list(set(refdScores))
	#print refdScores[0]
	#print refdScores[len(refdScores)-1]
	n1 = 0 - n
	refdScores = refdScores[n1:]
	#for item in refdScores:
		#print item[1]
	return refdScores
	

	
def selectThresholdNodes(concept, d, k):
	refdScores = []
	refdScores = sorted(d[concept].items(),key = operator.itemgetter(1))
	print refdScores[len(refdScores)-1]
	index1 = [n for n,i in enumerate(refdScores) if i[1]>=k]
	if len(index1)<>0:
		index = index1[0]
		newIndex = index - len(refdScores)
		refdScores = refdScores[newIndex:]
	else:
		refdScores = []
	return refdScores



f2 = open("/home/prajna/neo4j/input/inputConceptsToGenerateEqualRefDTrees")


inputConcepts = []


for line in f2:
	line = line[:-1]
	inputConcepts.append(line.replace(" ","_").lower())
f2.close()

threshList = [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
		
for concept in inputConcepts:
	for n in threshList:
		print concept
		input1 = []
		d = {}
		f = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/nodes/"+concept)
		f1 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+concept)
		
		
		o = open("/home/prajna/neo4j/input/refDTrees/latestRefDTrees/preqTreeRefD_thresh_top_5_"+str(n)+"_"+concept,"w")
		for line in f:
			line = line[:-1]
			input1.append(line)
		for item in input1:
			#print item
			d[item] = {}
		for line in f1:
			line = line[:-1]
			splitLine = line.split("\t")
			d[splitLine[0]]={}
			d[splitLine[1]]={}
			d[splitLine[0]][splitLine[1]] = 0.0
			d[splitLine[1]][splitLine[0]] = 0.0
		f1.close()
		f1 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+concept)
		for line in f1:
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
		preqTree = createRefDTreeWithThresholdAndTopk(concept,d, n)
		for key in preqTree.keys():
			
			if len(preqTree[key])<>0:
				#print key
				for item in preqTree[key]:
					o.write(str(item)+"\t"+str(key)+"\t"+str(d[item][key])+"\n")
		f.close()
		f1.close()
		o.close()
		
	

''''
for i in range(0,len(input1)-1,1):
	#print i
	for j in range(i+1,len(input1),1):
		d[input1[i]][input1[j]] = 0
for i in range(0,len(input1)-1,1):
	for j in range(i+1,len(input1),1):
		print d[input1[i]][input1[j]]
'''
