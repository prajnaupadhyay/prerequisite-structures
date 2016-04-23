#inputConcepts = ["concurrency_control","foreign_key","functional_dependency","query_plan","query_optimization","referential_integrity","scapegoat_tree"]
import sys
from os import listdir
from os.path import isfile, join

mypath = sys.argv[1]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for f in onlyfiles:
	print f
	f1 = open(mypath+f)
	#concept = f[f[:f.rfind("_")].rfind("_") + 1:]
	f3 = open("/home/prajna/neo4j/input/toposortTrees/inlinksInformation/inlinks")
	o = open("/home/prajna/neo4j/input/toposortTrees/csvFilesForHTML/"+f+".csv","w")
	
	dict1 = {}
	d = {}
	
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
		score = splitline[2]
		o.write(source+"_"+str(dict1[source])+","+target+"_"+str(dict1[target])+","+str(score)+"\n")
	f1.close()
	#f2.close()
	f3.close()
	o.close()
		
