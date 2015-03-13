from src.item import Interval , Server , Affectation

def tokenize ( lines ) :

	for line in lines :

		for item in line.split( ) :

			yield item


def take ( tokens , n ) :

	for i in range( n ) :

		yield int( next( tokens ) )


def header ( tokens ) :

	return take( tokens , 5 )


def problem ( tokens ) :

	R , S , U , P , M = header( tokens )

	rows = [ [ True ] * S for i in range( R ) ]

	servers = [ ]

	intervals = [ ]

	for i in range( U ) :

		# for each non available emplacement

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

				interval = Interval( r , j , size )

				intervals.append( interval )

			while i < S and not row[i] :

				i += 1


	for m in range( M ) :

		# for each server

		z , c = take( tokens , 2 )

		server = Server( m , c , z )

		servers.append( server )


	return R , S , U , P , M , intervals , servers , rows


def affectations ( lines ) :

	for line in lines :

		tokens = line.split( )

		if len( tokens ) != 3 : yield tuple( tokens )

		else : yield tuple( map( int , tokens ) )


def solution ( tuples , problem = None ) :

	if problem is None : raise Exception( "cannot parse solution without problem" )

	affectations = [ ]

	R , S , U , P , M , intervals , servers , _ = problem

	rows = [ [ ] for i in range ( R ) ]

	for interval in intervals :

		rows[interval.row].append( interval )

	skip = ( 'x' , )

	tuples = list( tuples )

	if len( tuples ) != M :

		raise Exception( "The number of lines of a solution should be M. Expected %d, received %d" % ( M , len( tuples ) ) )

	for i , values in enumerate( tuples ) :

		if values == skip : continue

		if len( values ) != 3 :

			raise Exception( "each line of a solution should contain 3 integers" )

		r , position , group = values

		if not 0 <= r < R :

			raise Exception( "invalid row" )

		if not 0 <= group < P :

			raise Exception( "invalid group" )

		row = rows[r]

		interval = next( ( interval for interval in row if interval.start <= position < interval.start + interval.size ) , None )

		if interval is None :

			raise Exception( "could not find interval" )

		server = next( ( server for server in servers if server.id == i ) , None )

		if server is None :

			raise Exception( "could not find server" )

		position -= interval.start

		if not 0 <= position < S :

			raise Exception( "invalid slot position" )

		affectation = Affectation( server , interval , position , group )

		affectations.append( affectation )

	return affectations
