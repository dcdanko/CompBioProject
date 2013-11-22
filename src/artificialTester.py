from ArtificialDataGenerator import ArtificialPhylogeny
from PyGrimmInterface import GrimmInterface

def fastRobinsonFouldsDistance(a,b):

	# Trees are represented as tuples (0, (1, (2, (3,4))))

	labels = {}

	def recursive_labeling(val, parts):
		if(type(val) is int):
			if(val in labels):
				return labels[val]
			else:
				labels[val] = randint(0,2**64)
				return recursive_labeling(val,parts)
		else:
			assert len(val) == 2
			newPartition = recursive_labeling(val[0], parts) ^ recursive_labeling(val[1], parts)
			if(type(parts)  == dict):
				parts[ newPartition ] = True
			else:
				parts.append(newPartition)
			return newPartition

	aParts = {}
	recursive_labeling(a, aParts)
	bParts = {}
	recursive_labeling(b, bParts)
	distance = 0
	for val in aParts:
		if val not in bParts:
			distance += 1
	
	return distance

def testOne():
	a = ArtificialPhylogeny
	for arb in range(5):
		a.evolve()

#	fastRobinsonFouldsDistance(a.tree,)

def grimmTest():
	a = ArtificialPhylogeny()
	genomes = []
	while(len(a.tree.getTips()) < 10):
		a.evolve()	
	for tip in  a.tree.getTips():
		genomes.append(tip.genome)	

	grimm = GrimmInterface()
	estimatedroot = grimm.findRootViaUPGMA(genomes)
	original = a.original

	transformations = grimm.getTransformations(estimatedroot, original)
	distance = len(transformations)-1
	print "estimate: "+str(estimatedroot)
	print distance


grimmTest()

