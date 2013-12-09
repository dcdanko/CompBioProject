from realTester import testHarness
from genome import Genome

inputfile = open('mammalInputFile.txt', 'r')
genomestring = inputfile.read()
genomestring = genomestring.strip()

splitgenomes = filter(None, genomestring.split(">"))
for i in xrange(len(splitgenomes)):
	splitgenomes[i] = ">"+splitgenomes[i]

genomes = [0 for x in xrange(len(splitgenomes))]
phylogeny = ()

for genome in splitgenomes:
	g = Genome(grimmString=genome)
	print("Scanned" )

	#put genomes in order for phylogeny construction
	if "Homo_sapiens" in genome:
		genomes[0] = g
	elif "Pan_troglodytes" in genome:
		genomes[1] = g
	elif "Macaca_mulatta" in genome:
		genomes[2] = g
	elif "Mus_musculus" in genome:
		genomes[3] = g
	elif "Rattus_norvegicus" in genome:
		genomes[4] = g
	elif "Bos_taurus" in genome:
		genomes[5] = g
	elif "Canis_lupus_familiaris" in genome:
		genomes[6] = g
	
phylogeny = ((((genomes[0],genomes[1]),genomes[2]),(genomes[3],genomes[4])),(genomes[5],genomes[6]))

(upgmaScore, upgmaRF, nniScores, nniRFs, conScore, conRF, maxRF) = testHarness(genomes, phylogeny)

print "upgmaScore: "+str(upgmaScore)
print "upgmaRF: "+str(upgmaRF)
print "nniScores: "+str(nniScores)
print "nniRFs: "+str(nniRFs)
print "conScore: "+str(conScore)
print "conRF: "+str(conRF)
print "maxRF: "+str(maxRF)

