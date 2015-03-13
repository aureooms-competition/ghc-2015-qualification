
from src import fd

from itertools import zip_longest

def read( filename , *processors , additional = None ) :

	if additional is None : additional = [ ]

	with open( filename ) as f :

		current = fd.lines( f )

		for processor , kwargs in zip_longest( processors , additional , fillvalue = None ) :

			if kwargs is None : current = processor( current )
			else : current = processor( current , **kwargs )

		return current
