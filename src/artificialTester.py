from ArtificialDataGenerator import ArtificialPhylogeny
from PyGrimmInterface import GrimmInterface
from upgma_tree import UPGMA
from genome import Genome
from Tree import Tree
import random as rn
from nni import doNNI

def fastRobinsonFouldsDistance(a,b):

	# Trees are represented as tuples (0, (1, (2, (3,4))))

	labels = {}

	def recursive_labeling(val, parts):
		if(type(val) is Tree):
			if(val in labels):
				return labels[val]
			else:
				labels[val] = rn.randint(0,2**64)
				return recursive_labeling(val,parts)
		else:
			if len(val) != 2:
				print( val)
				raise Exception("Val is wrong length")
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



def testUPGMA(cSize,depth):
	a = ArtificialPhylogeny(size=cSize,numChromosomes=10)
	for arb in range(depth):
		a.evolve()

	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	rf = fastRobinsonFouldsDistance(a.tree.toTuple(), u.tree.toTuple())
	return (rf, len( u.tree ) - 3)


def testNNI(cSize,depth):
	a = ArtificialPhylogeny(size=cSize,numChromosomes=10)
	while len( a.tree.getTips() ) < depth:
		a.evolve()

	if not a.tree.isBinary():
		print len(a.tree)
		print [ t.genome.getName() for t in a.tree.getTips()]
		print a.tree.allNodes()
		print a.tree
		raise Exception("Artificial Phylogeny is not binary")


	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	tree = u.tree 
	assert tree.isBinary()

	uRF = fastRobinsonFouldsDistance(a.tree.toTuple(), tree.toTuple())
	uScore = tree.getScore()
	doNNI( tree )
	nScore = tree.getScore()
	nRF = fastRobinsonFouldsDistance(a.tree.toTuple(), tree.toTuple())

	return (nRF, uRF, len(tree) - 3, uScore, nScore)


def grimmTest():
	a = ArtificialPhylogeny(size=2*1000,numChromosomes=10)
	genomes = []
	while(len(a.tree.getTips()) < 25):
		a.evolve()	
	for tip in  a.tree.getTips():
		genomes.append(tip.genome)	

	grimm = GrimmInterface()
	estimatedroot = grimm.findRootViaUPGMA(genomes)
	original = a.original

	transformations = grimm.getTransformations(estimatedroot, original)
	distance = len(transformations)-1
	# print "estimate: "+str(estimatedroot)
	print "GRIMM Distance: {}".format(distance)

# grimmTest()
if __name__ == "__main__":
	# val = 0.0
	# maxSize = 0.0
	# k = 20
	# for arb in range(k):
	# 	(a,b) = testUPGMA(100,5)
	# 	val += a
	# 	maxSize += b
	# print ( val/k, maxSize/k)
	
	nVal, uVal = 0.0, 0.0
	maxSize = 0.0
	k = 20
	for arb in range(k):
		(a,b,c,d,e) = testNNI(100,12)
		print (a,b,c,d,e)
		nVal += a
		uVal += b
		maxSize += c
	print ( nVal/k, uVal/k, maxSize/k)


