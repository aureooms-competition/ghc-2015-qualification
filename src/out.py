
from src import key


def writeFile( M , affectations ) :
	'''server, interval, position, group'''

	if not M : return

	f = open( 'out/out' , 'w' )
	
	affectations = sorted( affectations , key = key.id )

	with open( 'out/out' , 'w' ) :

		j = 0

		for i in range( M ) :

			if j < len( affectations ) :

				affectation = affectations[j]

				if affectation.id == i :

					pos = affectation.position + affectation.interval.start
					row = affectation.interval.row

					line = "{} {} {}\n".format(i, pos, row)
					j += 1

				else : line = 'x\n'

			else : line = 'x\n'

			f.write( line )

