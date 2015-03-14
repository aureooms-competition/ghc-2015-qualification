from src import key
from src import eval
from src import allocate
from src import groupchange

from random import randint , shuffle , sample

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


def firstfit ( servers , intervals , iterations = 1 ) :

	best = [ ]
	affectations = [ ]

	bestScore = 0
	score = 0

	for i in range( iterations ) :

		shuffle( servers )

		affectations = affect( servers , intervals )
		score = allocate.score( affectations )

		if score > bestScore :

			print( "number of affectations : " , len( affectations ) )
			best = affectations
			bestScore = score

	return best



def localsearch ( R , P , solution , iterations = 1 , swaps = 2 ) :

	affectations = solution.affectations
	groups = solution.groups
	rows = solution.rows
	best = solution.objective

	A = len( affectations )

	swaps = min( swaps , A )

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

		if objective > best :

			solution.objective = best = objective

			yield solution

		elif objective < best :

			for affectation , grp , old in zip( sample , grps , olds ) :

				affectation.group = old

				capacity = affectation.server.capacity

				groups[old] += capacity
				groups[grp] -= capacity

				rows[affectation.interval.row][old] += capacity
				rows[affectation.interval.row][grp] -= capacity



def vnd ( solution , pivoting , ordering ) :

	k = 0

	O = len( ordering )

	while k < O :

		best = pivoting( solution , ordering[k].walk , ordering[k].eval )

		while best.first :

			opt += best.first
			ordering[k].eval( solution , best.second )
			ordering[k].apply( solution , best.second )

			k = 0
			best = pivoting( solution , ordering[k].walk , ordering[k].eval )

		k += 1


def ii ( solution , pivoting , walk , eval , apply ) :

	while True :

		mutation , objective = pivoting( solution , walk , eval )

		if mutation is None : break

		apply( solution , mutation )

		solution.objective = objective

		yield solution


def optimize ( R , P , solution ) :

	affectations = solution.affectations

	groups = solution.groups
	rows = solution.rows

	while True :

		y , small = eval.poorest( groups , rows )

		solution.objective = small

		yield solution

		guaranteed = list( enumerate( eval.guaranteed( groups , rows ) ) )

		shuffle( guaranteed )

		for x , big in guaranteed :

			if x == y : continue

			available = list( filter( lambda a : a.group == x and big - a.server.capacity >= small , affectations ) )

			if not available : continue

			affectation = sample( available , 1 )[0]

			groupchange.apply( solution , ( affectation , y ) )

			break

		else : break
