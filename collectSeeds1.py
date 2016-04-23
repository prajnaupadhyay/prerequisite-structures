import urllib

f1 = open("/home/pearl/fromOlivaw/neo4jbackup/input/1.csv")
f2 = open("/home/pearl/fromOlivaw/neo4jbackup/input/CS.edges")
f3 = open("/home/pearl/fromOlivaw/neo4jbackup/input/CS.edges_neg")
f4 = open("/home/pearl/fromOlivaw/neo4jbackup/input/MATH.edges")
f5 = open("/home/pearl/fromOlivaw/neo4jbackup/input/MATH.edges_neg")
f6 = open("/home/pearl/fromOlivaw/neo4jbackup/input/inputConceptsToKnowLength")
f7 = open("/home/pearl/fromOlivaw/neo4jbackup/input/inputConceptsToKnowLength1")
o = open("/home/pearl/fromOlivaw/neo4jbackup/output/seedList","w")

seedList = []

'''
for line in f1:
	line = line[:-1]
	splitLine = line.split(",")
	concept1 = splitLine[len(splitLine)-7].replace('"','').lower()
	concept2 = splitLine[len(splitLine)-9].replace('"','').lower()
	seedList.append(urllib.unquote(concept1))
	seedList.append(urllib.unquote(concept2))
'''

for line in f2:
	line = line[:-1]
	splitLine = line.split("\t")
	seedList.append(urllib.unquote(splitLine[0].replace(" ","_").lower()))
	seedList.append(urllib.unquote(splitLine[1].replace(" ","_").lower()))
	
for line in f3:
	line = line[:-1]
	splitLine = line.split("\t")
	seedList.append(urllib.unquote(splitLine[0].replace(" ","_").lower()))
	seedList.append(urllib.unquote(splitLine[1].replace(" ","_").lower()))

for line in f4:
	line = line[:-1]
	splitLine = line.split("\t")
	seedList.append(urllib.unquote(splitLine[0].replace(" ","_").lower()))
	seedList.append(urllib.unquote(splitLine[1].replace(" ","_").lower()))
	
for line in f5:
	line = line[:-1]
	splitLine = line.split("\t")
	seedList.append(urllib.unquote(splitLine[0].replace(" ","_").lower()))
	seedList.append(urllib.unquote(splitLine[1].replace(" ","_").lower()))
	
for line in f6:
	line = line[:-1]
	seedList.append(urllib.unquote(line.replace(" ","_").lower()))
	
for line in f7:
	line = line[:-1]
	seedList.append(urllib.unquote(line.replace(" ","_").lower()))
	

seedList = list(set(seedList))
seedList.sort()
for item in seedList:
	o.write(item+"\n")
