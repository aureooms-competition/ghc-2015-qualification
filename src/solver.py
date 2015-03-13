from src import key
from src import eval
from random import randint , shuffle

import random

from src.item import Affectation


def affect ( servers , intervals ) :

	intervals = sorted( intervals , key = key.row )

	affectations = []

	available = [ interval.size for interval in intervals ]

	for server in servers :

		for i , interval in enumerate( intervals ) :

			if available[i] >= server.size :

				available[i] -= server.size
				affectation = Affectation( server , interval , available[i] )
				affectations.append( affectation )
				break

	return affectations


def scoreAffectations ( affectations ) :

	return sum( affectation.server.capacity for affectation in affectations )


def firstfit ( servers , intervals , iterations = 1 ) :

	best = []
	res = []

	bestScore = 0
	score = 0

	for i in range( iterations ) :

		shuffle( servers )

		res = affect( servers , intervals )
		score = scoreAffectations( res )

		if score > bestScore :

			print( "number of affectations : " , len( res ) )
			best = res
			bestScore = score

	return best

def localsearch ( R , P , affectations , iterations = 1 , swaps = 2 ) :

	A = len( affectations )

	swaps = min( swaps , A )

	for affectation in affectations :

		affectation.group = randint( 0 , P - 1 )

	groups , rows = eval.tableau(  R , P , affectations )

	best = eval.objective( groups , rows )

	for i in range( iterations ) :

		if iterations >= 100 and not i % ( iterations // 100 ) :
			print( "%3d%%   score = %d" % ( 100 * i / iterations , best ) )

		sample = random.sample( affectations , swaps )

		grps = [ randint( 0 , P - 1 ) for affectation in sample ]

		olds = [ affectation.group for affectation in sample ]

		for affectation , grp , old in zip( sample , grps , olds ) :

			affectation.group = grp

			capacity = affectation.server.capacity

			groups[old] -= capacity
			groups[grp] += capacity

			rows[affectation.interval.row][old] -= capacity
			rows[affectation.interval.row][grp] += capacity

		objective = eval.objective( groups , rows )

		if objective >= best :

			best = objective

		else :

			for affectation , grp , old in zip( sample , grps , olds ) :

				affectation.group = old

				capacity = affectation.server.capacity

				groups[old] += capacity
				groups[grp] -= capacity

				rows[affectation.interval.row][old] += capacity
				rows[affectation.interval.row][grp] -= capacity

	return affectations , best
