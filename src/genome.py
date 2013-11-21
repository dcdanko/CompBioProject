


class Genome( object ):

	def __init__( self, grimmString=""):
		self.grimmString = grimmString

	def getChromosoneArray( self ):
		g = []
		for line in self.grimmString.split("\n"):
			g += line.split("$")

		if ">" in g[0]:
			g = g[1:]

		return g

	def __iter__( self ):
		return iter( self.getChromosoneArray())

	def __str__( self ):
		return self.grimmString

	def addChromosone( self, chromosone ):
		if "$" not in chromosone:
			chromosone += " $"

		self.grimmString += "\n" + chromosone

	def addHeader( self, header ):
		if ">" not in self.getChromosoneArray()[0]:
			if ">" not in header:
				header = "> " + header
			self.grimmString = header + self.grimmString

	def name():
		return self.grimmString.split("\n")[0]
 
