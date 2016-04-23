inputConcepts = ["concurrency_control","foreign_key","functional_dependency","query_plan","query_optimization","referential_integrity","scapegoat_tree"]

for concept in inputConcepts:
	f1 = open("/home/prajna/neo4j/input/toposortTrees/subsetOfTrees/"+concept)
	f2 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+concept)
	f3 = open("/home/prajna/neo4j/input/toposortTrees/inlinksInformation/inlinks")
	o = open("/home/prajna/neo4j/input/toposortTrees/csvFilesForHTML/"+concept+"_firstParaLinks.csv","w")
	print concept
	
	dict1 = {}
	d = {}
	for line in f2:
		line = line[:-1]
		splitLine = line.split("\t")
		d[splitLine[0]]={}
		d[splitLine[1]]={}
		d[splitLine[0]][splitLine[1]] = 0.0
		d[splitLine[1]][splitLine[0]] = 0.0
	f2.close()
	f2 = open("/home/prajna/neo4j/input/refdScores/refdScores2_"+concept)
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
				
	for line in f3:
		line = line[:-1]
		splitline = line.split("\t")
		dict1[splitline[0]] = int(splitline[1])
	o.write("source,target,type\n")
	for line in f1:
		line = line[:-1]
		splitline = line.split("\t")
		source = splitline[0]
		target = splitline[1]
		if source in d.keys():
			if target in d[source].keys():
				o.write(source+"_"+str(dict1[source])+","+target+"_"+str(dict1[target])+","+str(d[source][target])+"\n")
	f1.close()
	f2.close()
	f3.close()
	o.close()
		
