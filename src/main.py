import fileinput
import argparse
import os.path
import signal
import sys
import itertools

from src import fd , action , parse , out , file , key

from src.ascii import valid , warning , error

from src import init , allocate , solver , optimizer , eval

from src import pivoting , neighborhood , destruct

from src import knapsack , datacenter

from src.item import Affectation , Solution


def firstfit ( args , problem , affectations = None ) :

	return solver.firstfit( problem.servers , problem.intervals , iterations = args.firstfit )


def roundrobin ( args , problem , affectations = None ) :

	servers = sorted( problem.servers , key = lambda x : x.capacity / x.size , reverse = True )

	tourniquet = allocate.maketourniquet( problem.R , problem.intervals )

	affectations = [ [ ] for interval in problem.intervals ]

	available = [ interval.size for interval in problem.intervals ]

	recycled = allocate.roundrobin( problem.R , servers , tourniquet , available , affectations )

	if args.recycle : allocate.recycle( problem.R , recycled , tourniquet , available , affectations )

	return sum( affectations , [ ] )

def knpsck ( args , problem , affectations = None ) :

	D = len( problem.intervals )
	N = len( problem.servers )
	v = [ server.capacity for server in problem.servers ]
	w = [ server.size for server in problem.servers ]
	W = [ interval.size for interval in problem.intervals ]

	print( D , N , len(v) , len(w) , len(W) , v , w , W )

	lp = knapsack.multidimensional( D , N , v , w , W )

	knapsack.solve( D , N , lp )

	solution = knapsack.solution( D , N , lp )

	affectations = [ ]

	for interval in problem.intervals :

		available = interval.size

		for server in problem.servers :

			if not next( solution ) : continue

			available -= server.size

			affectation = Affectation( server , interval , available )

			affectations.append( affectation )

	return affectations


def dtcntr ( args , problem , affectations = None ) :

	problem.intervals = sorted( problem.intervals , key = key.row )

	D = len( problem.intervals )
	N = len( problem.servers )
	R = problem.R
	P = problem.P

	ROW = [ [ ] for r in range ( R ) ]

	i = 0

	for k , g in itertools.groupby( problem.intervals , key.row ) :

		g = list( g )

		j = i + len( g )

		ROW[k] = [ index for index in range( i , j ) ]

		i = j

	v = [ server.capacity for server in problem.servers ]
	w = [ server.size for server in problem.servers ]
	W = [ interval.size for interval in problem.intervals ]

	print( D , N , R , P , len(v) , len(w) , len(W) , len(ROW) , v , w , W , ROW )

	lp = datacenter.problem( D , N , R , P , v , w , W , ROW )

	if affectations is not None :

		SRV = [ None ] * N

		ins = problem.intervals

		for i , server in enumerate( problem.servers ) :

			affectation = next( filter( lambda a : a.server.id == server.id , affectations ) , None )

			if affectation is None : continue

			st = affectation.interval.start

			d = next( ( d for ( d , _ ) in enumerate( ins ) if _.start == st ) , None )

			SRV[i] = ( d , affectation.group )

		datacenter.load( D , N , R , P , lp , SRV )



	print( "problem constructed" )

	datacenter.solve( D , N , R , P , lp )

	print( "solved" )

	solution = datacenter.solution( D , N , R , P , lp )

	affectations = [ ]

	for interval in problem.intervals :

		available = interval.size

		for server in problem.servers :

			for group in range( P ) :

				if not next( solution ) : continue

				available -= server.size

				affectation = Affectation( server , interval , available , group )

				affectations.append( affectation )

	return affectations


def noop ( args , problem , solution ) : return [ ]

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

def optimize ( args , problem , solution ) :

	while True :

		for _ , solution in zip( range( 50 ) , optimizer.optimize1( problem.R , problem.P , solution ) ) :

			yield solution

		for _ , solution in zip( range( 50 ) , optimizer.optimize2( problem.R , problem.P , solution ) ) :

			yield solution

		for _ , solution in zip( range( 50 ) , optimizer.optimize3( problem.R , problem.P , solution ) ) :

			yield solution

def ig ( args , problem , solution ) :

	wait = args.wait

	while True :

		solution.groups , solution.rows = eval.tableau( problem.R , problem.P , solution.affectations )
		solution.objective = current = eval.objective( solution.groups , solution.rows )

		print( current )

		localsearch = solver.ii(
			solution ,
			args.pivoting ,
			args.neighborhood.Walk( problem ) ,
			args.neighborhood.Eval( problem ) ,
			args.neighborhood.Apply( problem )
		)

		greedy2 = optimizer.optimize2 ( problem.R , problem.P , solution )
		greedy3 = optimizer.optimize3 ( problem.R , problem.P , solution )

		for step in localsearch , greedy2 , greedy3 :

			i = 0

			while i < wait :

				next( step )

				if solution.objective > current :

					current = solution.objective

					print( current )

					yield solution

					i = 0

				i += 1

		print( current )

		destruct.swap( solution , args.destruct )

		destruct.assign( problem.P , solution , args.destruct )



def optimize1 ( args , problem , solution ) :

	return optimizer.optimize1( problem.R , problem.P , solution )

def optimize2 ( args , problem , solution ) :

	return optimizer.optimize2( problem.R , problem.P , solution )

def optimize3 ( args , problem , solution ) :

	return optimizer.optimize3( problem.R , problem.P , solution )


FIRSTFIT = "firstfit"
ROUNDROBIN = "roundrobin"
KNAPSACK = "knapsack"
DATACENTER = "datacenter"

ALLOCATORS = {
	FIRSTFIT : firstfit ,
	ROUNDROBIN : roundrobin ,
	KNAPSACK : knpsck ,
	DATACENTER : dtcntr
}

LOCALSEARCH = "ls"
II = "ii"
IG = "ig"
OPT = "opt"
OPT1 = "opt1"
OPT2 = "opt2"
OPT3 = "opt3"
NOOP = "noop"

ALGORITHMS = {
	LOCALSEARCH : localsearch ,
	II : ii ,
	IG : ig ,
	OPT  : optimize ,
	OPT1 : optimize1 ,
	OPT2 : optimize2 ,
	OPT3 : optimize3 ,
	NOOP : noop
}

def solve ( ) :

	# parse args

	parser = argparse.ArgumentParser( )
	parser.add_argument( "input" , help = "input file" , type = str )
	parser.add_argument( "--load" , help = "existing solution to optimize" , type = str )
	parser.add_argument( "-a" , "--allocator" , help = "allocator to use" , type = str , choices = ALLOCATORS , action = action.Dict )
	parser.add_argument( "-i" , "--init" , help = "initializator to use" , type = str , choices = init.DICT , action = action.Dict , default = init.noop )
	parser.add_argument( "-r" , "--recycle" , help = "recycle unused servers" , action = "store_true" )
	parser.add_argument( "-f" , "--firstfit" , help = "# of iterations for first fit" , type = int , default = 100 )
	parser.add_argument( "-l" , "--localsearch" , help = "# of iterations for local search" , type = int , default = 100 )
	parser.add_argument( "-A" , "--algorithm" , help = "algorithm" , type = str , choices = ALGORITHMS , action = action.Dict , default =  noop )
	parser.add_argument( "-s" , "--swaps" , help = "# of items swapped at each iteration of the local search" , type = int , default = 2 )
	parser.add_argument( "-p" , "--pivoting" , help = "pivoting algorithm" , type = str , choices = pivoting.DICT , action = action.Dict )
	parser.add_argument( "-n" , "--neighborhood" , help = "neighborhood" , type = str , choices = neighborhood.DICT , action = action.Dict )
	parser.add_argument( "--write" , help = "write last solution" , action = "store_true" )
	parser.add_argument( "-w" , "--wait" , help = "# of unsuccessfull iterations before destruct" , type = int , default = 100 )
	parser.add_argument( "-d" , "--destruct" , help = "% of destruction" , type = float , default = 0.05 )
	parser.add_argument( "-m" , "--max" , help = "max size of servers" , type = int , default = 10000 )
	parser.add_argument( "-c" , "--copy" , help = "keep copy with special name" , type = str , default = None )
	args = parser.parse_args( )

	# parse problem

	problem = file.read( args.input , parse.tokenize , parse.problem )

	R = problem.R
	S = problem.S
	P = problem.P
	M = problem.M

	# initial solution

	affectations = None

	if args.load is not None :

		additional = ( None , { "problem" : problem } )
		affectations = file.read( args.load , parse.affectations , parse.solution , additional = additional )

	problem.servers = list( filter( lambda s : s.capacity <= args.max , problem.servers ) )

	# NOTE keep M unchanged for output

	problem.M = len( problem.servers )

	affectations = args.allocator( args , problem , affectations )

	print( "Servers : %d , Affectations : %d"  % ( problem.M , len( affectations ) ) )

	args.init( args , problem , affectations )


	# compute maximal possible score using this server affectation

	sa = ( 1 - 1 / R ) * sum( server.capacity for server in problem.servers ) / P
	ub = ( 1 - 1 / R ) * allocate.score( affectations ) / P

	print( "SA %f" % sa )

	print( "UB %f" % ub )

	# create evaluation tableau and solution state

	groups , rows = eval.tableau( R , P , affectations )

	objective = eval.objective( groups , rows )

	solution = Solution( affectations , groups , rows , objective )

	if args.write :

		def handler ( signal , frame ) :

			out.write( R , S , P , M , solution.affectations , solution.objective , copy = args.copy )

			sys.exit( 0 )

		signal.signal( signal.SIGINT , handler )

	# solve

	best = solution.objective

	for _ in args.algorithm( args , problem , solution ) :

		if solution.objective > best :

			best = solution.objective

			if out.improves( best ) :

				out.write( R , S , P , M , affectations , best , copy = args.copy )

			print( "[IMPROVED] %d" % best )

	affectations = solution.affectations
	objective = solution.objective

	print( "Final score : %d" % objective )
	print( "Final score : %d" % eval.all( R , P , affectations ) )

	if args.write : out.write( R , S , P , M , affectations , objective , copy = args.copy )

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

	for solution in sorted( args.solutions , key = out.objective ) :

		expected = out.objective( solution )

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
