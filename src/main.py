import fileinput
import argparse
import os.path

from src import fd , parse , allocate , solver , eval , out , file

def solve ( ) :

	# parse args

	parser = argparse.ArgumentParser( )
	parser.add_argument( "input" , help = "input file" , type = str )
	parser.add_argument( "-f" , "--firstfit" , help = "# of iterations for first fit" , type = int , default = 100 )
	parser.add_argument( "-l" , "--localsearch" , help = "# of iterations for local search" , type = int , default = 100 )
	parser.add_argument( "-s" , "--swaps" , help = "# of items swapped at each iteration of the local search" , type = int , default = 2 )
	args = parser.parse_args( )

	# parse problem

	problem = file.read( args.input , parse.tokenize , parse.problem )
	R , S , U , P , M , intervals , servers = problem

	# solve

	# affectations = solver.firstfit( servers , intervals , iterations = args.firstfit )

	servers = sorted( servers , key = lambda x : x.capacity / x.size , reverse = True )

	affectations = allocate.roundrobin( R , servers , intervals )

	print( "Servers : %d , Affectations : %d"  % ( M , len( affectations ) ) )

	affectations , objective = solver.localsearch( R , P , affectations , iterations = args.localsearch , swaps = args.swaps )

	print( "Final score : %d" % objective )
	print( "Final score : %d" % eval.all( R , P , affectations ) )

	out.write( M , affectations , objective )


def validate ( ) :

	# parse args

	parser = argparse.ArgumentParser( )
	parser.add_argument( "input" , help = "input file" , type = str )
	parser.add_argument( "solutions" , help = "solution files" , type = str , nargs = "+" )
	args = parser.parse_args( )

	# parse problem

	problem = file.read( args.input , parse.tokenize , parse.problem )
	R , S , U , P , M , intervals , servers = problem

	# validate solutions

	additional = ( None , { "problem" : problem } )

	for solution in args.solutions :

		expected = int( os.path.basename( solution ) )

		affectations = file.read( solution , parse.affectations , parse.solution , additional = additional )

		objective = eval.all( R , P , affectations )

		print( objective == expected , solution , objective )
