
from src import item

def all ( R , P , affectations ) :

	groups = [ 0 for i in range( P ) ]

	rows = [ [ 0 ] * P for i in range( R ) ]

	for affectation in affectations :

		g = affectation.group
		s = affectation.server
		i = affectation.interval

		groups[g] += s.capacity

		rows[i.row][g] += s.capacity

	return min( group - max( row[g] for row in rows ) for g , group in enumerate( groups ) )
