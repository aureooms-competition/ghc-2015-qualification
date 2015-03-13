import fileinput

from src import parse
from src import solver
from src import eval , out

def main ( ) :

	lines = fileinput.input( )

	tokens = parse.tokenize( lines )

	R , S , U , P , M , intervals , servers = parse.all( tokens )

	print ("result\n\n")

	affectations = solver.first_fit( servers , intervals , iterations = 1 )
	print ("Servers : ", M, "Affectations :",len(affectations))

	final_res = solver.affect_group_local_search(affectations, R, P)

	objective = eval.all( R , P , final_res  )

	out.write( M , final_res , objective )

