
class Genome( object ):

	def __init__( self, genome=None, grimmString=None, name=None, chromosomeList=None):

		if genome is not None:
			self.chromosomeList = genome.chromosomeList[:]
			self.name = genome.name + "_clone"
		else:
			self.chromosomeList = []
			self.name = name

			if grimmString != None:
				if name == None:
					grimmString = grimmString.strip()
					g = grimmString.split("\n")[0]
					if ">" in g:
						splitg = g.split()
						self.name = splitg[1]

				if chromosomeList == None:
					g = grimmString.split("\n")
					for line in g:
						if ">" in line or "#" in line:
							pass
						else:
							splitline = line.split()
							self.chromosomeList.append([int(val) for val in splitline if val != "$"])


	def __iter__( self ):
		return iter( self.chromosomeList)

	def __str__( self ):
		grimmString = "> "+self.name+" \n"
		for chromosome in self.chromosomeList:
			for val in chromosome:
				grimmString += str(val) + " "
			grimmString += "$ \n"
		return grimmString

		

	def addChromosome( self, chromosome ):
		if type(chromosome) is unicode:
			splitchrom = chromosome.split()
			self.chromosomeList.append([int(val) for val in splitchrom if val != "$"])

		elif type(chromosome) is list:
			self.chromosomeList.append(chromosome)

		else:
			raise Exception("Unexpected input to add chromosome")

	def getName(self,name=""):
		if name == "":
			return self.name
		else:
			self.name = name
			return self.name
 
