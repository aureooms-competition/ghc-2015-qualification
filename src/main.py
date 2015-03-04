
from .helloworld import helloworld

def main ( ) :

	print( helloworld )

	helloworld( )

	c = 0

	for i in range( 10000000 ) : c += i

	print( c )
