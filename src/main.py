
from src.helloworld import helloworld

import src.lp as lp

def main ( ) :

	print( main , helloworld )

	helloworld( )

	c = 0

	for i in range( 10000000 ) : c += i

	print( c )

	lp.test1( )
	lp.test2( )
