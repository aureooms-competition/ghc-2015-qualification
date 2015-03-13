
from src import key

def write ( M , affectations , objective ) :

	if not M : return

	affectations = sorted( affectations , key = key.serverid )

	with open( "out/%d" % objective  , "w" ) as f :

		j = 0
		A = len( affectations )

		fmt = "%d %d %d\n"
		notused = "x\n"

		for i in range( M ) :

			if j >= A : break

			affectation = affectations[j]

			if affectation.server.id == i :

				position = affectation.interval.start + affectation.position
				row = affectation.interval.row
				group = affectation.group

				line = fmt % ( row , position , group )
				j += 1

			else : line = notused

			f.write( line )


		while i < M :

			f.write( notused )
			i += 1

