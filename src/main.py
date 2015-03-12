
import fileinput

from src import parse

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

		print( server.id , server.capacity , server.size )
