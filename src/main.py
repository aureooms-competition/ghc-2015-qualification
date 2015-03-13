import fileinput

from src import parse
from src import affect_machines
from src import eval , out

def main ( ) :

	lines = fileinput.input( )

	tokens = parse.tokenize( lines )

	R , S , U , P , M , intervals , servers = parse.all( tokens )

	print( "R" , R )
	print( "S" , S )
	print( "U" , U )

	print( "P" , P )
	print( "M" , M )

	for interval in intervals :

		print( interval.row , interval.start , interval.size )

	for server in servers :

		print( server.capacity , server.size )


	print ("result\n\n")

	affectations = affect_machines.first_fit(servers, intervals)
	print ("Servers : ", M, "Affectations :",len(affectations))

	final_res = affect_machines.affect_group_local_search(affectations, R, P)
	print( server.id , server.capacity , server.size )

	objective = eval.all( R , P , final_res  )

	out.write( M , final_res , objective )

