from tempfile import NamedTemporaryFile
from genome import Genome
from subprocess import Popen, PIPE
import shlex
import upgma
import random

class GrimmInterface( object ):

	def genomeFile(self, genomes):
		gFile = NamedTemporaryFile(mode='w+')
		for genome in genomes:
			gFile.write( str( genome ))

		gFile.seek(0)

		return gFile


	def getTransformations( self, gA, gB):
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
				transformations.append( (line.split(":")[-1], Genome()) ) 
			elif line[-1] == "$":
				transformations[-1][1].addChromosome( line )
		return transformations



	def findRootViaUPGMA(self, genomes):
		distArray = self.getDistMatrix(genomes)

		genomeNames = [genome.name for genome in genomes]
		upgmatree = self.getUPGMA(distArray, genomeNames)
		genometree = self.genomeTree(upgmatree, genomes)
		
		#iterate through pairs in upgmatree	
		rootGenome = self.upgmaIterate(genometree)
		return rootGenome
			

        #input: a list of Genomes
	#output: the distance matrix obtained by running the genomes through GRIMM
	def getDistMatrix( self, genomes):
		gFile = self.genomeFile(genomes)
		print gFile.read()

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

		print grimmOut
		distArray = self.parseDistMatrix(grimmOut)
		return distArray


	def genomeTree(self, upgma, genomes):
		if(upgma.size == 1):
			for genome in genomes:
				if(genome.name == upgma.data):
					return genome
			#exception?
		else:
			left = self.genomeTree(upgma.data[0], genomes)
			right = self.genomeTree(upgma.data[1], genomes)
			return (left, right)
			


        #input: the string outputted by running GRIMM on more then 2 genomes
	#output: (genomes, distArray)
	#       genomes: a 1 dimensional array with the names of the genomes
	#       distArray: a 2 dimensional array rpresenting the genomes
        def parseDistMatrix(self, grimmout):

#                f = open(grimmfile, 'r')
#                output = f.read()
                distMatrix = grimmout.partition('Distance Matrix:')[2]
                distMatrix = distMatrix.strip()
                splitStr = distMatrix.split("\n")

                numGenomes = int(splitStr[0])
                #genomes = [0 for x in xrange(numGenomes)] 
                distArray = [ [0 for x in xrange(numGenomes)] for x in xrange(numGenomes)]
                for x in xrange(1, len(splitStr)):
                        splitMatrix = splitStr[x].split()
                        #genomes[x-1] = splitMatrix[0]
                        for y in xrange(1, len(splitMatrix)):
                                distArray[x-1][y-1] = float(splitMatrix[y]) 

#                return (genomes, distArray)
                return distArray

	def getUPGMA(self, distMatrix, genomeNames): 
		clu = upgma.make_clusters(genomeNames)
		tree = upgma.regroup(clu, distMatrix)
#		upgma.pprint(tree, tree.height)

		return tree

	def upgmaIterate(self, gtree):
		#if we have reached a 'leaf'
		if(type(gtree) != tuple):
			return gtree	
		else:
			left = self.upgmaIterate(gtree[0])
			right = self.upgmaIterate(gtree[1])
			trans = self.getTransformations(left, right)
			midIdx = len(trans)/2 #+ random.getrandbits(1)
			midGenome = trans[midIdx][1]
			midGenome.name = "("+str(left.name)+","+str(right.name)+")"
			return midGenome



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
