from ArtificialDataGenerator import ArtificialPhylogeny
from PyGrimmInterface import GrimmInterface
from upgma_tree import UPGMA
from genome import Genome
from Tree import Tree
import random as rn
from nni import NNI
import matplotlib.pyplot as plt
from pylab import savefig
from copy import deepcopy
from sys import setrecursionlimit
from consensusTree import ConsensusTree

def fastRFDist(a,b):

	# Trees are represented as tuples (0, (1, (2, (3,4))))

	labels = {}


	def recursive_labeling(val, parts):
		if type(val) is Tree  or type(val) is Genome:
			if type(val) is Tree:
				g = val.genome
			else:
				g = val

			if g in labels:
				return labels[g]
			else:
				labels[g] = rn.randint(0,2**64)
				return recursive_labeling(val,parts)
		else:

			newPartition = 0
			for v in val:
				newPartition = newPartition ^ recursive_labeling(v, parts)

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

def testHarness( genomes, actualPhylogeny ):

	u = UPGMA( genomes )
	u.calculate()
	print("Finished UPGMA")
	upgmaScore = u.tree.getScore()
	upgmaRF = fastRFDist( actualPhylogeny, u.tree.toTuple())

	n = NNI( u.tree )
	n.calculate()
	print("Finished NNI")
	nniScores = min([t.getScore() for t in n.trees])
	nniRFs = [fastRFDist( actualPhylogeny, t.toTuple()) for t in n.trees]

	c = ConsensusTree( n.trees )
	c.calculate()
	print("Finished Consensus")
	conScore = c.tree.getScore()
	conRF = fastRFDist( actualPhylogeny, c.tree.toTuple())

	maxRF = 2 * len(genomes) - 2

	return (upgmaScore, upgmaRF, nniScores, nniRFs, conScore, conRF, maxRF) 



