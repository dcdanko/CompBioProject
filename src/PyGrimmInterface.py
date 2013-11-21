from tempfile import NamedTemporaryFile
from genome import Genome
from subprocess import Popen, PIPE
import shlex

class PyGrimmInterface( object ):

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
				transformations[-1][1].addChromosone( line )
		return transformations



        #input: a list of Genomes
	#output: the distance matrix obtained by running the genomes through GRIMM
	def getDistMatrix( self, genomes):
		gFile = self.genomeFile(genomes)

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


        #input: the file outputted by running GRIMM on more then 2 genomes
	#output: (genomes, distArray)
	#       genomes: a 1 dimensional array with the names of the genomes
	#       distArray: a 2 dimensional array rpresenting the genomes
        def parseDistMatrix(grimmfile):

                f = open(grimmfile, 'r')
                output = f.read()
                distMatrix = output.partition('Distance Matrix:')[2]
                distMatrix = distMatrix.strip()
                splitStr = distMatrix.split("\n")

                numGenomes = int(splitStr[0])
                genomes = [0 for x in xrange(numGenomes)] 
                distArray = [ [0 for x in xrange(numGenomes)] for x in xrange(numGenomes)]
                for x in xrange(1, len(splitStr)):
                        splitMatrix = splitStr[x].split()
                        genomes[x-1] = splitMatrix[0]
                        for y in xrange(1, len(splitMatrix)):
                                distArray[x-1][y-1] = float(splitMatrix[y]) 

                return (genomes, distArray)




def main():
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
	
	grimm = PyGrimmInterface()

	grimm.getDistMatrix([Genome(gA), Genome(gB)])

##	k = grimm.getTransformations(Genome(gA),Genome(gB))
##	print(k)
