
import os , os.path

from src import key

OUT = "out"

MAGIC = 982451653

def blueprint ( R , S , P , affectations ) :

	hash = 0

	for affectation in affectations :

		hash *= S
		hash += affectation.interval.start + affectation.position
		hash %= MAGIC
		hash *= R
		hash += affectation.interval.row
		hash %= MAGIC
		hash *= P
		hash += affectation.group
		hash %= MAGIC

	return hash


def objective ( solution ) :

	return int( os.path.basename( solution.split( "-" )[0] ) )


def improves ( obj ) :

	solutions = ( objective( solution ) for solution in os.listdir( OUT ) )

	return obj > max( solutions )


def write ( R , S , P , M , affectations , objective , copy = None ) :

	if not M : return

	affectations = sorted( affectations , key = key.serverid )

	hash = blueprint( R , S , P , affectations )

	names = [ "{0}/{1}-{2:x}".format( OUT , objective , hash ) ]

	if copy is not None :

		names.append( "{0}/{1}-{2}".format( OUT , objective , copy ) )

	for name in names :

		with open( name , "w" ) as f :

			j = 0
			A = len( affectations )

			fmt = "%d %d %d\n"
			notused = "x\n"

			i = 0

			while i < M :

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

				i += 1


			while i < M :

				f.write( notused )
				i += 1

