
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

	best = int( max( os.listdir( OUT ) , key = objective ) )

	return obj > best



def write ( R , S , P , M , affectations , objective ) :

	if not M : return

	affectations = sorted( affectations , key = key.serverid )

	hash = blueprint( R , S , P , affectations )

	with open( "{0}/{1}-{2:x}".format( OUT , objective , hash )  , "w" ) as f :

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

