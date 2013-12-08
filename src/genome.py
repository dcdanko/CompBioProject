
class Genome( object ):

	def __init__( self, genome=None, grimmString=None, name=None, chromosomeList=None):

		if genome is not None:
			self.chromosomeList = [chromosome[:] for chromosome in genome]
			if name == None:
				self.name = genome.name[:]
			else:
				self.name = name
		else:
			self.chromosomeList = []
			self.name = name

			if grimmString != None:
				if name == None:
					grimmString = grimmString.strip()
					g = grimmString.split("\n")[0]
					if ">" in g:
						splitg = g.split(">")
						self.name = splitg[-1]

				if chromosomeList == None:
					g = grimmString.split("\n")
					for line in g:
						if ">" in line or "#" in line:
							pass
						else:
							splitline = line.split()
							self.chromosomeList.append([int(val) for val in splitline if val != "$"])
		if self.name is None:
			assert False

	def __len__( self):
		return len(self.chromosomeList)

	def __iter__( self ):
		return iter( self.chromosomeList)

	def __str__( self ):
		grimmString = "> "+self.name+" \n"
		for chromosome in self.chromosomeList:
			for val in chromosome:
				grimmString += str(val) + " "
			grimmString += "$ \n"
		return grimmString

	def __hash__(self):
		k = sorted( self.chromosomeList)
		out =  hash(str(k))
		return out
		

	def addChromosome( self, chromosome ):
		if ((type(chromosome) is unicode) or (type(chromosome) is str)):
			splitchrom = chromosome.split()
			for val in splitchrom:
				if (val != "$"):
					self.chromosomeList.append([int(val)])

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
 
