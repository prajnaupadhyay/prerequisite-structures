#parses a mediawiki dump and creates another dump containing only the first paragraph content

import re
import nltk.data

out = open("/home/prajna/neo4j/output/onlyFirstParaFirstLineLarge.xml","w")
f = open("/home/prajna/neo4j/output/onlyFirstParaLarge.xml")
#out1 = open("/home/prajna/neo4j/scripts/debugger","w")
textFlag = False
sectionFlag = False
commentFlag = False
pattern = re.compile("[\W]*==.*==[\W]*")
textPattern = re.compile("[\W]*(<text.*>.*)")
textClosePattern = re.compile("(.*)</text.*>")
commentPattern = re.compile("[\W]*<comment>.*")
commentClosePattern = re.compile("[\W]*.*</comment>")
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
count = 0
for line in f:
	count = count + 1
	if count%1000000 == 0:
		print count
	if(commentPattern.match(line) is not None):
		out.write(line)
		commentFlag = True
		if(commentClosePattern.match(line) is not None):
			commentFlag = False
	elif commentClosePattern.match(line) is not None:
		out.write(line)
		commentFlag = False
	#if(commentPattern.match(line) is None):
	elif commentFlag == True:
		out.write(line)
	else:
		if(textPattern.match(line) is None and textFlag==False and sectionFlag == False and commentFlag == False):
			#print line
			out.write(line)
			#out1.write(line+"\t"+str(textPattern.match(line) is None)+"\t"+str(textFlag)+"\t"+str(sectionFlag)+"\n")
		if textPattern.match(line) is None and textFlag == True and sectionFlag == False and pattern.match(line) is None and textClosePattern.match(line) is None and commentFlag == False:
			textPart = textPart + line
			#out1.write(line+"\t"+str(textPattern.match(line) is None)+"\t"+str(textFlag)+"\t"+str(sectionFlag)+"\n")
			#print line
		if pattern.match(line) is not None and textFlag == True and commentFlag == False:
			#print "section starts"
			sectionFlag = True
			#out.write(line)
			#print line
		if textPattern.match(line) is not None and commentFlag == False:
			#print line
			textPart = ""
			textFlag = True
			m = textPattern.match(line)
			textPart = textPart + m.group(1)
			#out.write(line)
			if textClosePattern.match(line) is not None and textFlag == True and commentFlag == False:
				textFlag = False
				sectionFlag = False
				out.write(textPart)
		elif textClosePattern.match(line) is not None and textFlag == True and commentFlag == False:
			#print line
			m = textClosePattern.match(line)
			textPart = textPart + m.group(1)
			s = '-----'.join(tokenizer.tokenize(textPart))
			s1 = s.split('-----')
			out.write(s1[0]+"</text>")
			textFlag = False
			sectionFlag = False
			#print line
			#out.write(line)
	
	
	
f.close()
out.close()
	
