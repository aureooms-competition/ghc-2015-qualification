from src import key
from src import eval
from src import allocate
from src import groupchange , serverswap , slotswap

import random , itertools

from random import randint , shuffle , sample


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


def optimize1 ( R , P , solution ) :

	affectations = solution.affectations

	groups = solution.groups
	rows = solution.rows

	while True :

		y , small = eval.poorest( groups , rows )

		solution.objective = small

		yield solution

		guaranteed = list( eval.guaranteed( groups , rows ) )

		shuffle( guaranteed )

		for x , big in guaranteed :

			if x == y : continue

			available = list( filter( lambda a : a.group == x and big - a.server.capacity >= small , affectations ) )

			if not available : continue

			affectation = sample( available , 1 )[0]

			groupchange.apply( solution , ( affectation , y ) )

			break

		else : break


def optimize2 ( R , P , solution ) :

	affectations = solution.affectations

	groups = solution.groups
	rows = solution.rows

	while True :

		y , small = eval.poorest( groups , rows )

		solution.objective = small

		yield solution

		ry , vy = eval.worst( rows , y )

		rwsy = list( eval.rows( rows , y ) )

		guaranteed = list( eval.guaranteed( groups , rows ) )

		shuffle( guaranteed )

		done = False

		for x , big in guaranteed :

			if x == y : continue

			rwsx = list( eval.rows( rows , x ) )

			for rx , vx in sorted( rwsx , key = key.second , reverse = True ) :

				avx = filter( lambda a : a.interval.row == rx , affectations )
				avy = filter( lambda a : a.interval.row == ry , affectations )

				avs = filter( lambda t : t[0].server.size == t[1].server.size , itertools.product( avx , avy ) )
				avc = filter( lambda t : t[0].server.capacity == t[1].server.capacity , itertools.product( avx , avy ) )

				if process( solution , avs , rwsx , rwsy , rx , ry , vx , vy , slotswap.apply ) :

					done = True
					break

				if process( solution , avc , rwsx , rwsy , rx , ry , vx , vy , serverswap.apply ) :

					done = True
					break

			if done : break

		else : break


def optimize3 ( R , P , solution ) :

	affectations = solution.affectations

	groups = solution.groups
	rows = solution.rows

	changed = True

	while changed :

		# changed = False

		y , small = eval.poorest( groups , rows )

		poors = list( filter( lambda t : t[1] == small , eval.guaranteed( groups , rows ) ) )

		y , small = poors[ randint( 0 , len( poors ) - 1 ) ]

		solution.objective = small

		yield solution

		for affectation in sorted( affectations , key = lambda x : x.group ) :

			x = affectation.group

			if x == y : continue

			r = affectation.interval.row
			worst1 , worst2 = eval.worst2( rows , x )

			w1 , worst1 = worst1
			w2 , worst2 = worst2

			if r != w1 :

				updated = groups[x] - worst1 - affectation.server.capacity

			else :

				updated = min( groups[x] - worst1 , groups[x] - worst2 - affectation.server.capacity )

			if updated <= small : continue

			print( "apply" , x , y , r , w1 , updated , small )

			groupchange.apply( solution , ( affectation , y ) )

			changed = True


def process ( solution , available , rwsx , rwsy , rx , ry , vx , vy , apply ) :

	for ax , ay in available :

		cx = ax.server.capacity
		cy = ay.server.capacity

		if rwsx[ry][1] + 2 * cx  <= vx and rwsy[rx][1] + 2 * cy <= vy :

			apply( solution , ( ax , ay ) )

			return True

	return False

