

def lines ( fd ) :

	return ( line[:-1] for line in iter( fd.readline , "" ) )
