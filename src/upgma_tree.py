import numpy as np
from PyGrimmInterface import GrimmInterface as Grimm
from Tree import Tree
from genome import Genome

def getMatrixMin(matrix):
	print "matrix in upgmatree: "+str(matrix)
	(width, height) = matrix.shape
	minimum, x, y = -1,0,0
	for i in range(width):
		for j in range(i+1, height):
			if minimum == -1 or matrix[i,j] < minimum:
				minimum = matrix[i,j]
				x, y= i, j
	print "x in upgmatree: "+str(x)
	print "y in upgmatree: "+str(y)
	print
	assert x != y
	return (x,y)

class UPGMA( object ):

	def __init__(self, genomes):
		self.grimm = Grimm()
		self.genomes = genomes
		self.distances = self.grimm.getDistMatrix( genomes )
		self.trees = [Tree(g) for g in genomes]

	def calculate(self):
		if len( self.trees) == 1:
			self.tree = self.trees[0]

		else:

			while len(self.trees) > 2:
				print "genomes in UPGMA: "+str(self.genomes)
				print "genome 2: "+str(self.genomes[1])
				t,g = len(self.trees), len(self.genomes)
				i,j = getMatrixMin(self.distances)
				print "i,j: "+str(i)+" "+str(j)

				newGenome = self.grimm.midGenome(self.genomes[i], self.genomes[j])
				print "new genome: "+str(newGenome)

				newTree = Tree( newGenome )
				newTree.addConnection( self.trees[i] )
				newTree.addConnection( self.trees[j] )

				self.trees[i] = newTree
				self.trees.pop(j)

				self.genomes[i] = newGenome
				self.genomes.pop(j)

				# self.distances = self.grimm.getUpdatedDistMatrix( self.genomes, self.distances, (i,j) )
				self.distances = self.grimm.getDistMatrix( self.genomes )
				print "self.distances: "+str(self.distances)
				if t - 1 != len(self.trees) or g - 1 != len(self.genomes):
					print newGenome
					print newTree
					print (i,j)
					print self.genomes
					print self.trees
					raise Exception

			if len( self.trees) == 2:
				self.tree = self.trees[0]
				self.tree.addConnection( self.trees[1] )

			else:
				print newGenome
				print newTree
				print (i,j)
				print self.trees
				print self.genomes
				raise Exception

			assert self.tree.isBinary()


