from src import key
from src import eval
from random import randint
from random import shuffle

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

def localsearch ( R , P , affectations , iterations = 1 ) :

	A = len( affectations )

	best = 0

	for affectation in affectations :

		group = randint( 0 , P - 1 )
		affectation.group = group

	for i in range( iterations ) :

		if iterations >= 100 and not i % ( iterations // 100 ) :
			print( "%d%%   score = %d" % ( 100 * i / iterations , best ) )

		aff1 = randint( 0 , A - 1 )
		aff2 = randint( 0 , A - 1 )

		grp1 = randint( 0 , P - 1 )
		grp2 = randint( 0 , P - 1 )

		old1 = affectations[aff1].group
		old2 = affectations[aff2].group

		affectations[aff1].group = grp1
		affectations[aff2].group = grp2

		objective = eval.all( R , P , affectations )

		if objective >= best :

			best = objective

		else :

			affectations[aff1].group = old1
			affectations[aff2].group = old2

	return affectations , best
