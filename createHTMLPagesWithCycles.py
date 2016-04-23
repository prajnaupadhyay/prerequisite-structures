import sys
import re

f1 = open("/home/prajna/neo4j/input/toposortTrees/prunedOnRefD/JSONFiles/part1")
f2 = open("/home/prajna/neo4j/input/toposortTrees/prunedOnRefD/JSONFiles/part2")
f3 = open("/home/prajna/neo4j/input/toposortTrees/prunedOnRefD/JSONFiles/part3")
f4 = open("/home/prajna/neo4j/input/toposortTrees/prunedOnRefD/JSONFiles/part4")
f5 = open("/home/prajna/neo4j/input/toposortTrees/prunedOnRefD/JSONFiles/lastPart")
#f6 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTreesAllLinks/onlyBackEdges")
#f7 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/onlyBackEdges")

inputConcepts = ["concurrency_control","foreign_key","functional_dependency","query_optimization","query_plan","referential_integrity","scapegoat_tree"]
onlyThreshList = [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
onlyDegree = [5, 10]
threshlistAndDegree = [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
onlyThreshList.sort()
onlyDegree.sort()
threshlistAndDegree.sort()

firstPart = ""
secondPart = ""
thirdPart = ""
fourthPart = ""
lastPart = ""

for line in f1:
	firstPart = firstPart + line
	
for line in f2:
	secondPart = secondPart + line
	
for line in f3:
	thirdPart = thirdPart + line
	
for line in f4:
	fourthPart = fourthPart + line
	
for line in f5:
	lastPart = lastPart + line
	
firstPart = firstPart[:-1]
secondPart = secondPart[:-1]
thirdPart = thirdPart[:-1]
fourthPart = fourthPart[:-1]
lastPart = lastPart[:-1]

htmlStr = ""

for snakeCaseItem in inputConcepts:
	o = open("htmlPagesNewer/"+snakeCaseItem+".html","w")
	#s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', concept)
	#snakeCaseItem = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
	orgJsonFile1 = "jsonFiles/"+snakeCaseItem+"_firstPara_treeEdges.json"
	orgJsonFile2 = "jsonFiles/"+snakeCaseItem+"_allLinks_treeEdges.json"
	jsonFile1 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/onlyBackEdges/"+snakeCaseItem+"_onlyBackEdges")
	cycleList1 = ""
	for line in jsonFile1:
		line = line[:-1]
		splitline = line.split("\t")
		cycleList1 = cycleList1 + "("+splitline[0]+", "+splitline[1]+"), "
	jsonFile2 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTreesAllLinks/onlyBackEdges/"+snakeCaseItem+"_onlyBackEdges")
	cycleList2 = ""
	for line in jsonFile2:
		line = line[:-1]
		splitline = line.split("\t")
		cycleList2 = cycleList2 + "("+splitline[0]+", "+splitline[1]+"), "
	readingOrder1 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/ReadingOrder/"+snakeCaseItem+"_firstParaLinks")
	readingList1 = "("
	for line in readingOrder1:
		line = line[:-1]
		splitline = line.split(",")
		readingList1 = readingList1  + splitline[0][2:-1] + ", "
	readingList1 = readingList1 + ")"
	readingOrder2 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTreesAllLinks/ReadingOrder/"+snakeCaseItem+"_allLinks")
	#o.write(firstPart+snakeCaseItem+secondPart+snakeCaseItem+thirdPart+orgJsonFile)
	readingList2 = "("
	for line in readingOrder2:
		line = line[:-1]
		splitline = line.split(",")
		readingList2 = readingList2  + splitline[0][2:-1] + ", "
	readingList2 = readingList2 + ")"
	readingOrder1.close()
	readingOrder2.close()
	
	htmlStr = htmlStr + firstPart+snakeCaseItem+"_firstParaLinks\").append(\"p\").text(\" Cycle List: "+cycleList1+"\").append(\"p\").text(\" Reading order: "+readingList1+thirdPart+orgJsonFile1+fourthPart+snakeCaseItem+"_allLinks\").append(\"p\").text(\" Cycle List: "+cycleList2+"\").append(\"p\").text(\" Reading order: "+readingList2+thirdPart+orgJsonFile2
	
	#o.write(firstPart+snakeCaseItem+secondPart+snakeCaseItem+thirdPart+orgJsonFile)
	#htmlStr = htmlStr + firstPart+snakeCaseItem+"_firstParaLinks\n Cycle List: "+cycleList1+"\n\n"+thirdPart+orgJsonFile1+fourthPart+snakeCaseItem+"_allLinks"+thirdPart+orgJsonFile2
	
	for thresh in onlyDegree:
		jsonFile = "jsonFiles/preqTreeRefD_degree_"+str(thresh)+"_"+snakeCaseItem+"_treeEdges.json"
		readingOrder1 = open("/home/prajna/neo4j/input/refDTrees/latestRefDTrees/ReadingOrder/preqTreeRefD_degree_"+str(thresh)+"_"+snakeCaseItem)
		readingList1 = "("
		for line in readingOrder1:
			line = line[:-1]
			splitline = line.split(",")
			readingList1 = readingList1  + splitline[0][2:-1] + ", "
		readingList1 = readingList1 + ")"
		readingOrder1.close()
		index1 = onlyDegree.index(thresh)
		#if index1<len(onlyDegree) - 1:
		#o.write(fourthPart+snakeCaseItem+" pruned by "+str(thresh)+thirdPart+jsonFile)
		htmlStr = htmlStr + fourthPart+snakeCaseItem+" refd top "+str(thresh)+"degree trees \").append(\"p\").text(\" Reading order: "+readingList1+thirdPart+jsonFile
		#elif onlyDegree.index(thresh) == len(onlyDegree) - 1:
		#print thresh
		#print lastPart
		#o.write(fourthPart+snakeCaseItem+" pruned by"+str(thresh)+thirdPart+jsonFile+lastPart)
		#htmlStr = htmlStr + fourthPart+snakeCaseItem+" pruned by"+str(thresh)+thirdPart+jsonFile+lastPart
	#htmlStrNew = htmlStr.replace("<p>Referential integrity Graphs</p>","<p>"+concept+" Graphs</p>")
	
	for thresh in onlyThreshList:
		jsonFile = "jsonFiles/preqTreeRefD_thresh_"+str(thresh)+"_"+snakeCaseItem+"_treeEdges.json"
		readingOrder1 = open("/home/prajna/neo4j/input/refDTrees/latestRefDTrees/ReadingOrder/preqTreeRefD_thresh_"+str(thresh)+"_"+snakeCaseItem)
		readingList1 = "("
		for line in readingOrder1:
			line = line[:-1]
			splitline = line.split(",")
			readingList1 = readingList1  + splitline[0][2:-1] + ", "
		readingList1 = readingList1 + ")"
		readingOrder1.close()
		index1 = onlyThreshList.index(thresh)
		#if index1<len(onlyThreshList) - 1:
		##o.write(fourthPart+snakeCaseItem+" pruned by "+str(thresh)+thirdPart+jsonFile)
		htmlStr = htmlStr + fourthPart+snakeCaseItem+" with threshold "+str(thresh)+"\").append(\"p\").text(\" Reading order: "+readingList1+thirdPart+jsonFile
		#elif onlyThreshList.index(thresh) == len(onlyThreshList) - 1:
		#print thresh
		#print lastPart
		#o.write(fourthPart+snakeCaseItem+" pruned by"+str(thresh)+thirdPart+jsonFile+lastPart)
		#htmlStr = htmlStr + fourthPart+snakeCaseItem+" pruned by"+str(thresh)+thirdPart+jsonFile+lastPart
	#htmlStrNew = htmlStr.replace("<p>Referential integrity Graphs</p>","<p>"+concept+" Graphs</p>")
	
	for thresh in threshlistAndDegree:
		for degree in onlyDegree:
			jsonFile = "jsonFiles/preqTreeRefD_thresh_top_"+str(degree)+"_"+str(thresh)+"_"+snakeCaseItem+"_treeEdges.json"
			readingOrder1 = open("/home/prajna/neo4j/input/refDTrees/latestRefDTrees/ReadingOrder/preqTreeRefD_thresh_top_"+str(degree)+"_"+str(thresh)+"_"+snakeCaseItem)
			readingList1 = "("
			for line in readingOrder1:
				line = line[:-1]
				splitline = line.split(",")
				readingList1 = readingList1  + splitline[0][2:-1] + ", "
			readingList1 = readingList1 + ")"
			readingOrder1.close()
			index1 = threshlistAndDegree.index(thresh)
			if index1<len(threshlistAndDegree) - 1:
			#o.write(fourthPart+snakeCaseItem+" pruned by "+str(thresh)+thirdPart+jsonFile)
				htmlStr = htmlStr + fourthPart+snakeCaseItem+" refd tree with threshold "+str(thresh)+" and top "+str(degree)+" links"+"\").append(\"p\").text(\" Reading order: "+readingList1+thirdPart+jsonFile
			elif threshlistAndDegree.index(thresh) == len(threshlistAndDegree) - 1 and onlyDegree.index(degree) == len(onlyDegree) - 1:
			#print thresh
				print lastPart
				#o.write(fourthPart+snakeCaseItem+" pruned by"+str(thresh)+thirdPart+jsonFile+lastPart)
				htmlStr = htmlStr + fourthPart+snakeCaseItem+" with threshold"+str(thresh)+" and top "+str(degree)+" links"+"\").append(\"p\").text(\" Reading order: "+readingList1+thirdPart+jsonFile+lastPart
	htmlStrNew = htmlStr.replace("<p>Referential integrity Graphs</p>","<p>"+snakeCaseItem+" Graphs</p>")
	o.write(htmlStrNew)
	htmlStrNew = ""
	htmlStr = ""
	o.close()
	jsonFile1.close()
	jsonFile2.close()
	
		
		
		
