import fileinput

from src import parse
from src import solver
from src import eval , out

def main ( ) :

	lines = fileinput.input( )

	tokens = parse.tokenize( lines )

	R , S , U , P , M , intervals , servers = parse.all( tokens )

	affectations = solver.firstfit( servers , intervals , iterations = 100 )

	print( "Servers : %d , Affectations : %d"  % ( M , len( affectations ) ) )

	affectations , objective = solver.localsearch( R , P , affectations , iterations = 100 )

	print( "Final score : %d" % objective )

	out.write( M , affectations , objective )

