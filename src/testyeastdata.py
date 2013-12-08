from realTester import testHarness
from genome import Genome

inputfile = open('yeastInputFile.txt', 'r')
genomestring = inputfile.read()
genomestring = genomestring.strip()

splitgenomes = filter(None, genomestring.split(">"))
for i in xrange(len(splitgenomes)):
	splitgenomes[i] = ">"+splitgenomes[i]

genomes = [0 for x in xrange(len(splitgenomes))]
phylogeny = ()

for genome in splitgenomes:
	g = Genome(grimmString=genome)

	#put genomes in order for phylogeny construction
	if "Saccharomyces_cerevisiae" in genome:
		genomes[0] = g
	elif "Eremothecium_gossypii" in genome:
		genomes[1] = g
	elif "Kluyveromyces_lactis" in genome:
		genomes[2] = g
	elif "Magnaporthe_oryzae" in genome:
		genomes[3] = g
	elif "Neurospora_crassa" in genome:
		genomes[4] = g
	elif "Schizosaccharomyces_pombe" in genome:
		genomes[5] = g
	elif "Caenorhabditis_elegans" in genome:
		genomes[6] = g
	
#phylogeny = ((((genomes[0], (genomes[1], genomes[2])),(genomes[3],genomes[4])),genomes[5]),genomes[6]) 
#phylogeny = (((((genomes[0], genomes[1]), genomes[2]),(genomes[3],genomes[4])),genomes[5]),genomes[6]) 
phylogeny = (((((genomes[0], genomes[2]), genomes[1]),(genomes[3],genomes[4])),genomes[5]),genomes[6]) 


(upgmaScore, upgmaRF, nniScores, nniRFs, conScore, conRF, maxRF) = testHarness(genomes, phylogeny)

print "upgmaScore: "+str(upgmaScore)
print "upgmaRF: "+str(upgmaRF)
print "nniScores: "+str(nniScores)
print "nniRFs: "+str(nniRFs)
print "conScore: "+str(conScore)
print "conRF: "+str(conRF)
print "maxRF: "+str(maxRF)

