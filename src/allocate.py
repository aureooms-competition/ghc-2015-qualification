
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


def maketourniquet ( R , intervals ) :

	tourniquet = Tourniquet( R )

	for i , interval in enumerate( intervals ) :

		tourniquet[interval.row].add( ( i , interval ) )

	return tourniquet


def roundrobin ( R , servers , tourniquet , available , affectations ) :

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

	return recycled

def recycle ( R , recycled , tourniquet , available , affectations ) :

	changed = True

	while changed :

		changed = False

		servers = recycled

		recycled = [ ]

		for server in servers :

			used = False

			for _ in range( R ) :

				i , interval = next( tourniquet )

				for j , oldaffectation in enumerate( affectations[i] ) :

					old = oldaffectation.server

					better = server.capacity > old.capacity

					if better and server.size <= available[i] + old.size :

						for k in range( j + 1 , len( affectations[i] ) ) :

							affectations[i][k].position += old.size

						available[i] += old.size
						available[i] -= server.size

						affectation = Affectation( server , interval , available[i] )

						affectations[i].pop( j )
						affectations[i].append( affectation )

						changed = True
						recycled.append( old )

						used = True
						break

				if used : break

			else : recycled.append( server )

	return recycled

