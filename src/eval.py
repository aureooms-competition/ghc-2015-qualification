
def objective( groups , rows ) :

	return min( group - max( row[g] for row in rows ) for g , group in enumerate( groups ) )

def tableau ( R , P , affectations ) :

	groups = [ 0 for i in range( P ) ]

	rows = [ [ 0 ] * P for i in range( R ) ]

	for affectation in affectations :

		g = affectation.group
		s = affectation.server
		i = affectation.interval

		groups[g] += s.capacity

		rows[i.row][g] += s.capacity

	return groups , rows


def all ( R , P , affectations ) :

	groups , rows = tableau( R , P , affectations )

	return objective( groups , rows )

