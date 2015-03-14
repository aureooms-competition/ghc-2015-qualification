
from src import key

def max2 ( iterable , key = None ) :

	"""

		>>> max2( )

	"""

	first = next( iterable , None )
	second = next( iterable , None )

	if second is None or first is None :

		return first , second

	if key( second ) > key( first ) :

		first , second = second , first

	for item in iterable :

		if key( item ) > key( first ) :

			second = first
			first = item

		elif key( item ) > key( second ) :

			second = item

	return first , second

def rows ( rws , g ) :

	return ( ( r , row[g] ) for r , row in enumerate( rws ) )

def worst ( rws , g ) :

	return max( rows( rws , g ) , key = key.second )

def worst2 ( rws , g ) :

	return max2( rows( rws , g ) , key = key.second )

def guaranteed ( groups , rows ) :

	return ( ( g , group - max( row[g] for row in rows ) ) for g , group in enumerate( groups ) )

def sorted ( groups , rows ) :

	return sorted( guaranteed( groups , rows ) , key = key.second )

def richest ( groups , rows ) :

	return max( guaranteed( groups , rows ) , key = key.second )

def poorest ( groups , rows ) :

	return min( guaranteed( groups , rows ) , key = key.second )

def objective ( groups , rows ) :

	return min( group - max( row[g] for row in rows ) for g , group in enumerate( groups ) )

def tableau ( R , P , affectations ) :

	groups = [ 0 for i in range( P ) ]

	rows = [ [ 0 ] * P for i in range( R ) ]

	for affectation in affectations :

		g = affectation.group
		server = affectation.server
		interval = affectation.interval
		r = interval.row

		groups[g] += server.capacity

		rows[r][g] += server.capacity

	return groups , rows


def all ( R , P , affectations ) :

	groups , rows = tableau( R , P , affectations )

	return objective( groups , rows )


