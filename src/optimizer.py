
import itertools

from random import randint , sample , shuffle

from src import key

from src import eval

from src import serverswap , groupchange , slotswap

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

