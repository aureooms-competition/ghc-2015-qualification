
from src.item import Affectation

class Pool :

	def __init__( self ) :

		self.current = -1
		self.pool = [ ]

	def add( self , item ) :

		self.pool.append( item )

	def __next__( self ) :

		self.current += 1

		if self.current == len( self.pool ) : self.current = 0

		return self.pool[self.current]

class Tourniquet :

	def __init__( self , R ) :

		self.current = -1
		self.pools = [ Pool( ) for _ in range( R ) ]

	def __getitem__( self , i ) :

		return self.pools[i]

	def __next__( self ) :

		self.current += 1

		if self.current == len( self.pools ) : self.current = 0

		return next( self.pools[self.current] )

def roundrobin ( R , servers , intervals ) :

	tourniquet = Tourniquet( R )

	for i , interval in enumerate( intervals ) :

		tourniquet[interval.row].add( ( i , interval ) )

	affectations = []

	available = [ interval.size for interval in intervals ]
	affectations = [ [ ] for interval in intervals ]

	#	changed = True
	#
	#	while changed :
	#
	#		changed = False
	#
	#		replaced = [ ]

	recycled = [ ]

	for server in servers :

		for _ in range( R ) :

			i , interval = next( tourniquet )

			if available[i] >= server.size :

				available[i] -= server.size
				affectation = Affectation( server , interval , available[i] )
				affectations[i].append( affectation )
				break

		else : recycled.append( server )

	changed = True

	while changed :

		changed = False

		server = recycled

		recycled = [ ]

		for server in servers :

			used = True

			for _ in range( R ) :

				i , interval = next( tourniquet )

				for j , oldaffectation in enumerate( affectations[i] ) :

					old = oldaffectation.server

					better = server.capacity > old.capacity

					if better and server.size <= available[i] + old.size :

						available[i] -= server.size - old.size
						affectation = Affectation( server , interval , available[i] )
						affectations[i][j] = affectation

						changed = True
						recycled.append( old )

						break

				else :

					used = False

				if used : break

			else : recycled.append( server )


	return sum( affectations , [ ] )

