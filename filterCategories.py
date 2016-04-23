f1 = open("/home/prajna/neo4j/input/yagoTransitiveType.tsv")
f2 = open("/home/prajna/neo4j/input/yagoSimpleTypes.tsv")
f3 = open("/home/prajna/neo4j/input/pageAndTheirCategoriesLarge")
f4 = open("/home/prajna/neo4j/input/conceptsFromSeeds")
o = open("/home/prajna/neo4j/output/filteredConceptsFromSeeds2","w")

wikiCategories = {}
categories = {}
conceptsFromSeeds = []
nodes = []

for line in f3:
	line = line[:-1]
	splitLine = line.split("\t")
	pageName = splitLine[0].replace(" ","_").lower()
	categoryName = splitLine[1].replace(" ","_").lower()
	if pageName not in wikiCategories:
		wikiCategories[pageName] = ""
	else:
		wikiCategories[pageName] = categoryName + "###" + wikiCategories[pageName]
for line in f1:
	line = line[:-1]
	splitLine = line.split("\t")
	pageName = splitLine[1].replace("<","").replace(">","").lower()
	categoryName = splitLine[3].replace("<","").replace(">","").lower()
	if pageName not in categories:
		categories[pageName] = ""
	else:
		categories[pageName] = categoryName+"###"+categories[pageName]
		
for line in f2:
	line = line[:-1]
	splitLine = line.split("\t")
	pageName = splitLine[1].replace("<","").replace(">","").lower()
	categoryName = splitLine[3].replace("<","").replace(">","").lower()
	if pageName not in categories:
		categories[pageName] = ""
	else:
		categories[pageName] = categoryName+"###"+categories[pageName]
for line in f4:
	line = line[:-1]
	conceptsFromSeeds.append(line)
print "\ndone reading categories"

for item in conceptsFromSeeds:
	if item in categories:
		if "person" not in categories[item] and "organization" not in categories[item] and "building" not in categories[item] and "yagoGeoEntity" not in categories[item]:
			#outputFiles[counter].write(str(item[0].encode('utf-8'))+"\t")
			if item in wikiCategories:
				if "people" not in wikiCategories[item] and "company" not in wikiCategories[item] and "companies" not in wikiCategories[item] and "country" not in wikiCategories[item] and "countries" not in wikiCategories[item] and "nation" not in wikiCategories[item] and "nations" not in wikiCategories[item] and "state" not in wikiCategories[item] and "states" not in wikiCategories[item]:
					nodes.append(item)
				else:
					continue
			else:
				nodes.append(item)	
		else:
			continue
	elif item in wikiCategories:
		if "people" not in wikiCategories[item] and "company" not in wikiCategories[item] and "companies" not in wikiCategories[item] and "country" not in wikiCategories[item] and "countries" not in wikiCategories[item] and "nation" not in wikiCategories[item] and "nations" not in wikiCategories[item] and "state" not in wikiCategories[item] and "states" not in wikiCategories[item]:
			nodes.append(item)
		else:
			continue
		#outputFiles[counter].write(str(item[0].encode('utf-8'))+"\t")
	else:	
		nodes.append(item)
		#continue
for item in nodes:
	o.write(item+"\n")	
