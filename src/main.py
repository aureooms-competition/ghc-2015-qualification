import fileinput
import argparse
import os.path

from src import fd , parse , allocate , init , solver , out , file

from src import pivoting , walk , eval , apply

from src.item import Solution

FIRSTFIT = "firstfit"
ROUNDROBIN = "roundrobin"


def firstfit (  args , problem ) :

	R , S , U , P , M , intervals , servers , rows = problem

	return solver.firstfit( servers , intervals , iterations = args.firstfit )


def roundrobin ( args , problem ) :

	R , S , U , P , M , intervals , servers , rows = problem

	servers = sorted( servers , key = lambda x : x.capacity / x.size , reverse = True )

	tourniquet = allocate.maketourniquet( R , intervals )

	affectations = [ [ ] for interval in intervals ]

	available = [ interval.size for interval in intervals ]

	recycled = allocate.roundrobin( R , servers , tourniquet , available , affectations )

	if args.recycle : allocate.recycle( R , recycled , tourniquet , available , affectations )

	return sum( affectations , [ ] )

LOCALSEARCH = "localsearch"
II = "ii"

def localsearch ( args , problem , solution  ) :

	R , S , U , P , M , intervals , servers , rows = problem

	return solver.localsearch( R , P , solution , iterations = args.localsearch , swaps = args.swaps )

def ii ( args , problem , solution ) :

	R , S , U , P , M , intervals , servers , rows = problem

	return solver.ii(
		solution ,
		pivoting.firstoreq ,
		walk.RandomGroupChange( P ) ,
		eval.groupchange ,
		apply.groupchange
	)

ALLOCATORS = { FIRSTFIT : firstfit , ROUNDROBIN : roundrobin }

ALGORITHMS = { LOCALSEARCH : localsearch , II : ii }

def solve ( ) :

	# parse args

	parser = argparse.ArgumentParser( )
	parser.add_argument( "input" , help = "input file" , type = str )
	parser.add_argument( "--solution" , help = "existing solution to optimize" , type = str )
	parser.add_argument( "-a" , "--allocator" , help = "allocator to use" , type = str , choices = ALLOCATORS , required = True )
	parser.add_argument( "-r" , "--recycle" , help = "recycle unused servers" , action = "store_true" )
	parser.add_argument( "-f" , "--firstfit" , help = "# of iterations for first fit" , type = int , default = 100 )
	parser.add_argument( "-l" , "--localsearch" , help = "# of iterations for local search" , type = int , default = 100 )
	parser.add_argument( "-A" , "--algorithm" , help = "# local search algorithm" , type = str , choices = ALGORITHMS , required = True )
	parser.add_argument( "-s" , "--swaps" , help = "# of items swapped at each iteration of the local search" , type = int , default = 2 )
	args = parser.parse_args( )

	# parse problem

	problem = file.read( args.input , parse.tokenize , parse.problem )
	R , S , U , P , M , intervals , servers , rows = problem

	# initial solution

	if args.solution is None :

		affectations = ALLOCATORS[args.allocator]( args , problem )

		print( "Servers : %d , Affectations : %d"  % ( M , len( affectations ) ) )

		init.random( P , affectations )

	else :

		additional = ( None , { "problem" : problem } )
		affectations = file.read( args.solution , parse.affectations , parse.solution , additional = additional )

	# create evaluation tableau and solution state

	grps , rws = eval.tableau( R , P , affectations )

	objective = eval.objective( grps , rws )

	solution = Solution( affectations , grps , rws , objective )

	# solve

	for _ in ALGORITHMS[args.algorithm]( args , problem , solution ) :

		print( solution.objective )

	affectations = solution.affectations
	objective = solution.objective

	print( "Final score : %d" % objective )
	print( "Final score : %d" % eval.all( R , P , affectations ) )

	out.write( R , S , P , M , affectations , objective )


def validate ( ) :

	# parse args

	parser = argparse.ArgumentParser( )
	parser.add_argument( "input" , help = "input file" , type = str )
	parser.add_argument( "solutions" , help = "solution files" , type = str , nargs = "+" )
	args = parser.parse_args( )

	# parse problem

	problem = file.read( args.input , parse.tokenize , parse.problem )
	R , S , U , P , M , intervals , servers , rows = problem

	# validate solutions

	additional = ( None , { "problem" : problem } )

	name = lambda solution : int( os.path.basename( solution.split( "-" )[0] ) )

	for solution in sorted( args.solutions , key = name ) :

		expected = name( solution )

		affectations = file.read( solution , parse.affectations , parse.solution , additional = additional )

		objective = eval.all( R , P , affectations )

		print( objective == expected , solution , objective )

		# validate

		slotsused = [ [ 0 ] * S for _ in range( R ) ]

		serversused = [ 0 ] * M

		for affectation in affectations :

			i = affectation.server.id
			r = affectation.interval.row
			position = affectation.interval.start + affectation.position

			serversused[i] += 1

			for j in range( position , position + affectation.server.size ) :

				slotsused[r][j] += 1

		for i , used in enumerate( serversused ) :

			if used > 1 :

				print( "[INFEASIBLE] Server %d used %d times" % ( i , used ) )

		for r , row , urow in zip( range( R ) , rows , slotsused ) :

			for i , available , used in zip( range( S ) , row , urow ) :

				authorized = 1 if available else 0

				if used > authorized :

					print( "[INFEASIBLE] Row %d , slot %d , used %d > %d times" % ( r , i , used , authorized ) )
