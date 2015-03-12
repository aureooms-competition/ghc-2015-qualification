
from src import key


def write( M , affectations , objective ) :
	'''server, interval, position, group'''

	if not M : return

	affectations = sorted( affectations , key = key.serverid )

	with open( 'out/%d' % objective  , 'w' ) as f :

		j = 0

		for i in range( M ) :

			if j < len( affectations ) :

				affectation = affectations[j]

				if affectation.server.id == i :

					pos = affectation.position + affectation.interval.start
					row = affectation.interval.row
					group = affectation.group

					line = "{} {} {}\n".format( row , pos , group )
					j += 1

				else : line = 'x\n'

			else : line = 'x\n'

			f.write( line )

