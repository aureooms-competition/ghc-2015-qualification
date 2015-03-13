
import functools

class Color ( object ) :

	HEADER = "\033[95m"
	OKBLUE = "\033[94m"
	OKGREEN = "\033[92m"
	WARNING = "\033[93m"
	FAIL = "\033[91m"
	ENDC = "\033[0m"
	BOLD = "\033[1m"
	UNDERLINE = "\033[4m"

def display ( msg , color = None ) :

	if color is None : print( msg )

	else : print( "%s%s%s" % ( color , msg , Color.ENDC ) )

valid   = functools.partial( display , color = Color.OKGREEN )
warning = functools.partial( display , color = Color.WARNING )
error   = functools.partial( display , color = Color.FAIL )
