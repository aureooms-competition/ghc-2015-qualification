

from random import randint , sample , shuffle

from src import eval

class RandomWalk ( object ) :

	def __init__ ( self , problem ) :

		self.P = problem.P

	def __call__ ( self , solution ) :

		affectations = solution.affectations

		A = len( affectations )

		P = self.P

		while True :

			yield affectations[ randint( 0 , A - 1 ) ] , randint( 0 , P - 1 )

class ShuffledWalk ( object ) :

	def __init__ ( self , problem ) :

		self.P = problem.P

	def __call__ ( self , solution ) :

		affectations = solution.affectations

		swaps = [ ( affectation , g ) for affectation in affectations for g in range( self.P ) ]

		shuffle( swaps )

		yield from swaps


class Eval ( object ) :

	def __init__ ( self , problem ) : pass

	def __call__ ( self , solution , mutation ) :

		groups = solution.groups
		rows = solution.rows

		affectation , grp = mutation

		old = affectation.group

		capacity = affectation.server.capacity

		groups[old] -= capacity
		groups[grp] += capacity

		rows[affectation.interval.row][old] -= capacity
		rows[affectation.interval.row][grp] += capacity

		obj = eval.objective( solution.groups , solution.rows )

		groups[old] += capacity
		groups[grp] -= capacity

		rows[affectation.interval.row][old] += capacity
		rows[affectation.interval.row][grp] -= capacity

		return obj


class Apply ( object ) :

	def __init__ ( self , problem ) : pass

	def __call__ ( self , solution , mutation ) :

		groups = solution.groups
		rows = solution.rows

		affectation , grp = mutation

		old = affectation.group
		affectation.group = grp

		capacity = affectation.server.capacity

		groups[old] -= capacity
		groups[grp] += capacity

		rows[affectation.interval.row][old] -= capacity
		rows[affectation.interval.row][grp] += capacity




