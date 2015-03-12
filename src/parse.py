from src import item

def tokenize ( lines ) :

	for line in lines :

		for item in line.split( ) :

			yield item


def take ( tokens , n ) :

	for i in range( n ) :

		yield int( next( tokens ) )


def header ( tokens ) :

	return take( tokens , 5 )


def all ( tokens ) :

	R , S , U , P , M = header( tokens )

	rows = [ [ True ] * S for i in range( R ) ]

	servers = []

	intervals = []

	for i in range( U ) :

		# pour chaque emplacement non disponible

		r , s = take( tokens , 2 )

		rows[r][s] = False

	for r , row in enumerate( rows ) :

		# generate intervals for each row

		i = 0

		while i < S :

			size = 0
			j = i

			while i < S and row[i] :

				size += 1
				i += 1

			if size > 0 :

				intervals.append( item.Interval( r , j , size ) )

			while i < S and not row[i] :

				i += 1


	for m in range( M ) :

		# pour chaque serveur

		z , c = take( tokens , 2 )

		servers.append( item.Server( m , c , z ) )


	return R , S , U , P , M , intervals , servers


