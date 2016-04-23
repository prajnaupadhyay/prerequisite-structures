#parses a mediawiki dump and creates a table containing page titles and their categories

import re

out = open("/home/prajna/neo4j/output/pageAndTheirCategoriesLarge1","w")
f = open("/home/prajna/wikipediajan2016dump/enwiki-20151201-pages-articles-multistream.xml")
#out1 = open("/home/prajna/neo4j/scripts/debugger","w")
pageFlag = False
titleFlag = False
pattern = re.compile("\[\[Category:(.*)\]\].*")
pagePattern = re.compile("[\W]*<page.*")
pageClosePattern = re.compile(".*</page.*")
titlePattern = re.compile("[\W]*<title>(.*)</title>")
pageTitle = ""
categoryName = ""
count = 0
for line in f:
	count = count + 1
	if count%1000000 == 0:
		print count
	if(pagePattern.match(line) is not None and pageFlag == False):
		pageFlag = True
	if pageFlag == True:
		if(titlePattern.match(line) is not None):
			pageTitle = titlePattern.match(line).group(1)
			titleFlag = True
	if pageFlag == True and titleFlag == True and pattern.match(line) is not None:
		#print "here"
		categoryName = pattern.match(line).group(1)
		out.write(pageTitle +"\t"+categoryName +"\n")
	if pageFlag == True and titleFlag == True:
		if pageClosePattern.match(line) is not None:
			pageFlag = False
			titleFlag = False
			pageTitle = ""
			categoryName = ""
f.close()
out.close()
	
