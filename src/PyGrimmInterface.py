from tempfile import NamedTemporaryFile
import genome
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

		command = './../GRIMM/grimm -f {}'.format(gFile.name)

		grimm =  Popen(command, stdout=PIPE, stderr=PIPE, shell=True )
		try:
			grimmOut = grimm.communicate(timeout=15)[0].decode("utf-8")
		except:
			grimm.kill()
			raise new Exception("Communication with Grimm failed.")

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
				transformations[-1][0].addChromosone( line )
		return transformations




	def getDistMatrix( self, genomes):
		pass


def tests():
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

	k = grimm.getTransformations(gA,gB)
	print(k)


if __name__ == "__main__":
	tests()
