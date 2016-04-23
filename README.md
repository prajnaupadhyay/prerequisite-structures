# prerequisite-structures

1) extractCategories.py: parses a mediawiki dump and creates a table containing page titles and their categories

2) parseLargeDumpToget1stPara.py: parses a mediawiki dump and creates another dump containing only the first paragraph content

3) filterDataset.py: Filters the technical content out

4) createPandLXML.py: Fiters the techincal content out from the output returned from dizzy logic parser

5) collectSeeds1.py: Collects seed technical concepts into a single list

6) parse1stParaDumpToExtract1stLine.py: extracts first line from the first para mediawiki dump 

7) collectNeighboursForSeeds.py: Given an input list of concepts, it collects all concepts located at most two hops away from the input concept and stores them in a file

8) filterCategories.py: Filters the generated list of concepts from the previous step on the basis of Wikipedia and Yago categories and stores the result in a file

9) findRefDScoresForInputConcepts1.py: for a list of input concepts, does BFS and finds RefD for all the concepts located at most two hops away, stores the results in a file

10) saveNumberOfInlinks.py: Calculates the a) number of inlinks b) number of outlinks for an input concept and stores result in a file.

11) extract1stLine.py: Script to extract the first line of Wikipedia page from the dump of mediawiki abstracts.

12) createPrerequisiteTrees.py: Creates prerequisite trees for an input concept using Topological sort concept considering all the links of a wikipedia page (or only the links coming out from the first paragraph)

13) extractRelevanceAndScope.py: Collects the nodes of prerequisite trees for all input concepts and retruns the following

a) jaccard similarity of the categories of the two nodes,
b) number of pages in the category having the same name as the node (page), 
c) number of subcategories in the category having the same name as the node (page), 
d) number of categories the node (page) belongs to

14) generateSubgraph.py: Returns the Wikipedia subgraph containing the links upto two hops for a list of input concepts and stores it in file.

15) pruneTreesBasedOnParameters.py: Given any tree as input, it prunes the tree based on the following parameters:

a) Reference distance between the root and other nodes: For threshold values from 0.02 to 0.9, it returns different trees pruned on them
b) Relevance between the root and other nodes (or jaccard similarity between the categories of the two nodes): For threshold values from 0.02 to 0.9, it returns different trees pruned on them
c) Scope difference between the root and every other node in the tree: This script uses scope as the number of inlinks for a node (page). For scope difference ranging from 10 to 50, it prunes the nodes of the original tree.

16) generateRefDTrees1.py: Generates RefD trees for an input concept in the following ways:

a) Level wise and top k: Generates RefD trees of level given as input by selecting the top k nodes as children
b) Level wise thresholded with r: Generates RefD trees of level given as input by selecting the nodes having higher RefD than r as children
c) Level wise and thresholded with r and with top k: Generates RefD trees of level given as input by selecting the top k nodes having higher RefD than r as children

17) generateReadingOrder.py: For a given input concept, generates the reading order. It first does the topological sort of the subgraph for the input concept. When cycles are discovered, the edge having the minimum RefD value is deleted from the graph and the reading order is returned accordingly.

18) createInputFilesForHTML.py: Converts the subgraph surrounding the input concept into a format required by d3 library (for force directed layout) to be rendered in a graph.

19) createInputFilesForHTMLRefD.py: Converts the RefD tree of the input concept into a format required by d3 library (for force directed layout) to be rendered in a graph.

20) createTreeAndOtherEdges.py: Stores the tree and back edges from the input graph of a concept to a file

21) createJSONGraphsWithCycles.py: Converts the tree edges into json format to be rendered into a d3 collapsible tree layout

22) createHTMLPagesWithCycles.py: Creates the html page that takes the json files as input to be rendered into a d3 collapsible tree layout. Includes the cycles and reading order in the html file itself.

23) findOnlyOneHopPathNodes.py: For an input concept, finds out the nodes that are located at a distance of one hop but do not have an edge to any of the neighbours of input concept

24) findConcepts3ormoreHopsAway.py: For an input concept, finds the nodes that are located at a shortest distance of 3 hops

25) findContradictions.py: Does the following
 a) Collect all the concepts located at most 2 hop distance away from the input concept 
 b) Find out RefD score for each of them and sort them in decreasing order
 c) Find out pairs for an input concept which are contradictory
