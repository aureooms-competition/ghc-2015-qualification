
from random import randint , sample , shuffle

class RandomGroupChange ( object ) :

	def __init__ ( self , P ) :

		self.P = P

	def __call__ ( self , solution ) :

		affectations = solution.affectations

		swaps = [ ( affectation , g ) for affectation in affectations for g in range( self.P ) ]

		shuffle( swaps )

		yield from swaps
