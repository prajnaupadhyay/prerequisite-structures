import time
import sys




def findScope(concept,o):
	if concept in pagesThatAreAlsoCategories:
		o.write(concept+"\t"+str(len(categoryDict[concept]))+"\t"+str(len(pageCategories[concept]))+"\t"+str(subcatsCategories[concept])+"\t"+str(numPagesCategories[concept])+"\n")
	else:
		o.write(concept+"\t0\t"+str(len(pageCategories[concept]))+"\t0\t0\n")
def findRelevance(concept1, concept2, o1):
	category1 = pageCategories[concept1]
	category2 = pageCategories[concept2]
	commonCategories = set(category1).intersection(category2)
	num = float(len(commonCategories))
	denom = float(len(category1)+len(category2)-len(commonCategories))
	if denom<>0:
		jaccardIndex = num/denom
	else:
		jaccardIndex = -9999
	o1.write(concept1+"\t"+concept2+"\t"+str(jaccardIndex)+"\n")

	
start_time = time.time()	
pageCategories = {}
categoryDict = {}
subcatsCategories = {}
numPagesCategories = {}

pagesThatAreAlsoCategories = []
pagesThatAreAlsoCategories1 = []
conceptList = []
prunedConceptList = []
inputFiles = []
f2 = open("/home/prajna/neo4j/scripts/latestTreesScripts/prunedConceptList")
for line in f2:
	line = line[:-1]
	prunedConceptList.append(line)
inputConcepts = ["concurrencyControl","foreignKey","functionalDependency","queryOptimization","queryPlan","referentialIntegrity","relationalModel","scapegoatTree"]
for item in inputConcepts:
	inputFiles.append("")
i = 0
for item in inputConcepts:
	inputFiles[i] = open("/home/prajna/neo4j/input/toposortTrees/"+item)
	for line in inputFiles[i]:
		line = line[:-1]
		splitLine = line.split("\t")
		conceptList.append(splitLine[0])
		conceptList.append(splitLine[1])
	inputFiles[i].close()
	i = i + 1
	
conceptList = list(set(conceptList))
for item in conceptList:
	pageCategories[item] = []
	categoryDict[item] = []
	subcatsCategories[item] = 0
	numPagesCategories[item] = 0
	
	
f = open("/home/prajna/neo4j/output/pageAndTheirCategoriesLarge1")
for line in f:
	line = line[:-1]
	if line[len(line)-1] == '|':
		line = line[:-1]
	splitlines = line.split("\t")
	pageName = splitlines[0].replace(" ","_").lower()
	categoryName = splitlines[1].replace(" ","_").lower()
	categoryDict[categoryName] = []
	pageCategories[pageName] = []
f.close()
f = open("/home/prajna/neo4j/output/pageAndTheirCategoriesLarge1")
for line in f:
	line = line[:-1]
	if line[len(line)-1] == '|':
		line = line[:-1]
	splitlines = line.split("\t")
	pageName = splitlines[0].replace(" ","_").lower()
	categoryName = splitlines[1].replace(" ","_").lower()
	categoryDict[categoryName].append(pageName)
	pageCategories[pageName].append(categoryName)

f1 = open("/home/prajna/wikipediajan2016dump/categoriesWithSubcategories")
for line in f1:
	line = line[:-1]
	splitLine = line.split("\t")
	categoryName = splitLine[0].replace(" ","_").lower()
	subcatsCategories[categoryName] = int(splitLine[2])
	numPagesCategories[categoryName] = int(splitLine[1])
	
pagesThatAreAlsoCategories1 = set(categoryDict.keys()).intersection(pageCategories.keys())
pagesThatAreAlsoCategories = set(subcatsCategories.keys()).intersection(pagesThatAreAlsoCategories1)





		
print len(pageCategories)
print len(categoryDict)
print time.time() - start_time


o = open("/home/prajna/neo4j/scripts/latestTreesScripts/output/scope1","w")
o1 = open("/home/prajna/neo4j/scripts/latestTreesScripts/output/relevance1","w")


for item in conceptList:
	findScope(item, o)
	
for i in range(1,len(prunedConceptList),1):
	for j in range(i+1,len(prunedConceptList),1):
		findRelevance(prunedConceptList[i], prunedConceptList[j], o1)



#findScope(sys.argv[1].replace(" ","_").lower())





