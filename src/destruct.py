
from src import slotswap

from random import random , randint


class Swap ( object ) :

	def __init__ ( self , args , problem ) :

		self.p = args.p

	def __call__ ( self , solution ) :

		swap( solution , self.p )


def swap ( solution , p ) :

	affectations = solution.affectations

	for ax in affectations :

		for ay in affectations :

			if ax.server.size == ay.server.size and random( ) < p :

				slotswap.apply( solution , ( ax , ay ) )

			if ax.server.capacity == ay.server.capacity and random( ) < p :

				slotswap.apply( solution , ( ax , ay ) )

class Assign ( object ) :

	def __init__ ( self , args , problem ) :

		self.P = problem.P
		self.p = args.p

	def __call__ ( self , solution ) :

		assign( self.P , solution , self.p )


def assign ( P , solution , p ) :

	affectations = solution.affectations

	for ax in affectations :

		if random( ) < p :

			ax.group = randint( 0 , P - 1 )
