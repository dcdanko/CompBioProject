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




	def getDistMatrix( self, genomes):
		pass






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
	
	grimm = PyGrimmInterface()

	k = grimm.getTransformations(Genome(gA),Genome(gB))
	print(k)
