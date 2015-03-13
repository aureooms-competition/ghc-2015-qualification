import fileinput
import argparse
import os.path

from src import fd , action , parse , out , file

from src.ascii import valid , warning , error

from src import init , allocate , solver , eval

from src import pivoting , neighborhood

from src.item import Solution


def firstfit ( args , problem ) :

	return solver.firstfit( problem.servers , problem.intervals , iterations = args.firstfit )


def roundrobin ( args , problem ) :

	servers = sorted( problem.servers , key = lambda x : x.capacity / x.size , reverse = True )

	tourniquet = allocate.maketourniquet( problem.R , problem.intervals )

	affectations = [ [ ] for interval in problem.intervals ]

	available = [ interval.size for interval in problem.intervals ]

	recycled = allocate.roundrobin( problem.R , servers , tourniquet , available , affectations )

	if args.recycle : allocate.recycle( problem.R , recycled , tourniquet , available , affectations )

	return sum( affectations , [ ] )

def localsearch ( args , problem , solution ) :

	return solver.localsearch( problem.R , problem.P , solution , iterations = args.localsearch , swaps = args.swaps )

def ii ( args , problem , solution ) :

	return solver.ii(
		solution ,
		args.pivoting ,
		args.neighborhood.Walk( problem ) ,
		args.neighborhood.Eval( problem ) ,
		args.neighborhood.Apply( problem )
	)

FIRSTFIT = "firstfit"
ROUNDROBIN = "roundrobin"

ALLOCATORS = { FIRSTFIT : firstfit , ROUNDROBIN : roundrobin }

LOCALSEARCH = "ls"
II = "ii"

ALGORITHMS = { LOCALSEARCH : localsearch , II : ii }

def solve ( ) :

	# parse args

	parser = argparse.ArgumentParser( )
	parser.add_argument( "input" , help = "input file" , type = str )
	parser.add_argument( "--solution" , help = "existing solution to optimize" , type = str )
	parser.add_argument( "-a" , "--allocator" , help = "allocator to use" , type = str , choices = ALLOCATORS , required = True , action = action.Dict )
	parser.add_argument( "-r" , "--recycle" , help = "recycle unused servers" , action = "store_true" )
	parser.add_argument( "-f" , "--firstfit" , help = "# of iterations for first fit" , type = int , default = 100 )
	parser.add_argument( "-l" , "--localsearch" , help = "# of iterations for local search" , type = int , default = 100 )
	parser.add_argument( "-A" , "--algorithm" , help = "algorithm" , type = str , choices = ALGORITHMS , required = True , action = action.Dict )
	parser.add_argument( "-s" , "--swaps" , help = "# of items swapped at each iteration of the local search" , type = int , default = 2 )
	parser.add_argument( "-p" , "--pivoting" , help = "pivoting algorithm" , type = str , choices = pivoting.DICT , action = action.Dict )
	parser.add_argument( "-n" , "--neighborhood" , help = "neighborhood" , type = str , choices = neighborhood.DICT , action = action.Dict )
	args = parser.parse_args( )

	# parse problem

	problem = file.read( args.input , parse.tokenize , parse.problem )

	R = problem.R
	S = problem.S
	P = problem.P
	M = problem.M

	# initial solution

	if args.solution is None :

		affectations = args.allocator( args , problem )

		print( "Servers : %d , Affectations : %d"  % ( M , len( affectations ) ) )

		init.random( P , affectations )

	else :

		additional = ( None , { "problem" : problem } )
		affectations = file.read( args.solution , parse.affectations , parse.solution , additional = additional )

	# create evaluation tableau and solution state

	groups , rows = eval.tableau( R , P , affectations )

	objective = eval.objective( groups , rows )

	solution = Solution( affectations , groups , rows , objective )

	# solve

	for _ in args.algorithm( args , problem , solution ) :

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

	R = problem.R
	S = problem.S
	P = problem.P
	M = problem.M

	# validate solutions

	additional = ( None , { "problem" : problem } )

	name = lambda solution : int( os.path.basename( solution.split( "-" )[0] ) )

	for solution in sorted( args.solutions , key = name ) :

		expected = name( solution )

		affectations = file.read( solution , parse.affectations , parse.solution , additional = additional )

		objective = eval.all( R , P , affectations )

		( valid if objective == expected else error )( "%s %d" % ( solution , objective ) )

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

				error( "[INFEASIBLE] Server %d used %d times" % ( i , used ) )

		for r , row , urow in zip( range( R ) , problem.rows , slotsused ) :

			for i , available , used in zip( range( S ) , row , urow ) :

				authorized = 1 if available else 0

				if used > authorized :

					error( "[INFEASIBLE] Row %d , slot %d , used %d > %d times" % ( r , i , used , authorized ) )
