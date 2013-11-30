from tempfile import NamedTemporaryFile
from genome import Genome
from subprocess import Popen, PIPE
import shlex
import upgma
import random as rn
import numpy as np

class GrimmInterface( object ):

	def __init__(self):
		self.matchedGenomes = {}

	def midGenome(self, gA, gB):
		trans = self.getTransformations(gA,gB)
		ind = len(trans)/2 
		return trans[ind][1]

	def genomeFile(self, genomes):
		gFile = NamedTemporaryFile(mode='w+')
		for genome in genomes:
			gFile.write( str( genome ))

		gFile.seek(0)

		return gFile

	def getDistance( self, gA, gB):
		tLen = len( self.getTransformations(gA,gB))
		if tLen == 1:
			return 0
		else:
			return tLen -2

	def getTransformations( self, gA, gB):

		if gA in self.matchedGenomes:
			if gB in self.matchedGenomes[gA]:
				return self.matchedGenomes[gA][gB]
				
		if gB in self.matchedGenomes:
			if gA in self.matchedGenomes[gB]:
				return self.matchedGenomes[gB][gA]

		gFile = self.genomeFile( [gA,gB] )

		command = "./../GRIMM/grimm -f {}".format(gFile.name)
		comman = shlex.split(command)
		grimm =  Popen(command, stdout=PIPE, shell=True )
		try:
			grimmOut = grimm.communicate()[0].decode("utf-8")
		except Exception as e:
			grimm.kill()
			print(e)
			raise Exception("Communication with Grimm failed.")

		gFile.close()


		grimmOut = grimmOut.split("======================================================================")
		grimmOut = grimmOut[-1]
		transformations = []
		for line in grimmOut.split("\n"):
			if len(line) == 0:
				pass
			elif line == "An optimal sequence of rearrangements:":
				pass
			elif "Step" in line:
				transformations.append( (line.split(":")[-1], Genome(name=str(rn.randint(0,2**64)))) ) 
			elif line[-1] == "$":
				transformations[-1][1].addChromosome( line )

		if gA in self.matchedGenomes:
			self.matchedGenomes[gA][gB] = transformations
		else:
			self.matchedGenomes[gA] = {gB:transformations}
		if gB in self.matchedGenomes:
			self.matchedGenomes[gB][gA] = transformations
		else:
			self.matchedGenomes[gB] = {gA:transformations}

		return transformations

			

		#input: a list of Genomes
	#output: the distance matrix obtained by running the genomes through GRIMM
	def getDistMatrix( self, genomes):
		gFile = self.genomeFile(genomes)
		assert type( genomes[0] ) == Genome
		# print gFile.read()

		command = "./../GRIMM/grimm -f {}".format(gFile.name)
		grimm =  Popen(command, stdout=PIPE, shell=True )
		try:
			grimmOut = grimm.communicate()[0].decode("utf-8")
		except Exception as e:
			grimm.kill()
			raise Exception("Communication with Grimm failed.")

		gFile.close()

		return self.parseDistMatrixIntoNP(grimmOut)

	def parseDistMatrixIntoNP( self, grimmOut ):
		grimmOut = grimmOut.partition('Distance Matrix:')[2]
		grimmOut = grimmOut.strip()
		grimmOut = grimmOut.split("\n")

		grimmOut = [line.split()[1:] for line in grimmOut][1:]

		matrix = np.empty( (len(grimmOut) , len(grimmOut)))
		for i, line in enumerate(grimmOut):
			for j, val in enumerate( line ):
				matrix[i,j] = val

		return matrix

	def getUpdatedDistMatrix( self, genomes, oldMatrix, (i,j)):
		dist = []
		for ind, g in enumerate(genomes):
			if ind != i:
				dist.append( len(self.getTransformations(g, genomes[i])))

		newMatrix = np.empty( (len(genomes), len(genomes)) )
		(width, height) = oldMatrix.shape

		for x in range(width):
			for y in range(height):
				if x == i:
					if y < j:
						newMatrix[x,y] = dist[y]
					elif y > j:
						newMatrix[x,y-1] = dist[y-1]
				elif y == i:
					if x < j:
						newMatrix[x,y] = dist[x]
					elif x > j:
						newMatrix[x-1,y] = dist[x-1]
				elif x < j and y < j:
					newMatrix[x,y] = oldMatrix[x,y]
				elif x < j and y > j:
					newMatrix[x, y-1] = oldMatrix[x, y]
				elif x > j and y < j:
					newMatrix[x-1,y] = oldMatrix[x,y]
				elif x > j and y > j:
					newMatrix[x-1,y-1] = oldMatrix[x,y]
				else:
					pass

		return newMatrix




if __name__ == "__main__":
	gA = '''
	> alpha
	1 2 3 4 $
	5 6 7 8 $
	'''

	gB = '''
	> beta
	1 6 3 8 $
	5 2 7 4 $
	'''

	gC = '''
	> gamma
	1 2 4 3 $
	5 6 7 8 $
	'''

	grimm = GrimmInterface()
	gnma = Genome(grimmString=gA)
	gnmb = Genome(grimmString=gB)
	gnmc = Genome(grimmString=gC)

	#rootGenome = grimm.findRootViaUPGMA([gnma,gnmb,gnmc])

	k = grimm.getTransformations(gnma, gnmb)
	print len(k)
	print(k)
