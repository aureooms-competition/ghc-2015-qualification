import fileinput
import argparse

from src import fd , parse , allocate , solver , eval , out

def main ( ) :

	# parse args

	parser = argparse.ArgumentParser( )
	parser.add_argument( "input" , help = "input file" , type = str )
	parser.add_argument( "-f" , "--firstfit" , help = "# of iterations for first fit" , type = int , default = 100 )
	parser.add_argument( "-l" , "--localsearch" , help = "# of iterations for local search" , type = int , default = 100 )
	parser.add_argument( "-s" , "--swaps" , help = "# of items swapped at each iteration of the local search" , type = int , default = 2 )
	args = parser.parse_args( )

	# parse problem

	with open( args.input ) as f :

		lines = fd.lines( f )

		tokens = parse.tokenize( lines )

		R , S , U , P , M , intervals , servers = parse.all( tokens )

	# solve

	# affectations = solver.firstfit( servers , intervals , iterations = args.firstfit )

	servers = sorted( servers , key = lambda x : x.capacity / x.size , reverse = True )

	affectations = allocate.roundrobin( R , servers , intervals )

	print( "Servers : %d , Affectations : %d"  % ( M , len( affectations ) ) )

	affectations , objective = solver.localsearch( R , P , affectations , iterations = args.localsearch , swaps = args.swaps )

	print( "Final score : %d" % objective )
	print( "Final score : %d" % eval.all( R , P , affectations ) )

	out.write( M , affectations , objective )

