import numpy as np
from PyGrimmInterface import GrimmInterface as Grimm
from Tree import Tree

def getMatrixMin(matrix):
	(width, height) = matrix.shape
	minimum, x, y = -1,0,0
	for i in range(width):
		for j in range(i+1, height):
			if minimum == -1 or matrix[i,j] < minimum:
				minimum = matrix[i,j]
				x, y= i, j
	return (x,y)

class UPGMA( object ):

	def __init__(self, genomes):
		self.grimm = Grimm()
		self.genomes = genomes
		self.distances = self.grimm.getDistMatrix( genomes )
		self.trees = [Tree(g) for g in genomes]

	def calculate(self):

		while len(self.trees) > 2:

			i,j = getMatrixMin(self.distances)

			newGenome = self.grimm.midGenome(self.genomes[i], self.genomes[j])

			newTree = Tree( newGenome )
			newTree.addConnection( self.trees[i] )
			newTree.addConnection( self.trees[j] )

			self.trees[i] = newTree
			self.trees.pop(j)

			self.genomes[i] = newGenome
			self.genomes.pop(j)

			# self.distances = self.grimm.getUpdatedDistMatrix( self.genomes, self.distances, (i,j) )
			self.distances = self.grimm.getDistMatrix( self.genomes )

		self.tree = self.trees[0]
		self.tree.addConnection( self.trees[1] )
