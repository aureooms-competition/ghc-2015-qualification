
import ecyglpki as glpk

def multidimensional ( D , N , v , w , W ) :

	x = lambda d , i  : d * N + i + 1

	lp = glpk.Problem( )

	lp.add_cols( D * N )

	lp.add_rows( D + N )

	for d in range( D ) :

		for i in range( N ) :

			lp.set_col_kind( x( d , i ) , "binary" )
			lp.set_obj_coef( x( d , i ) , v[i] )

		mapping = { x( d , i ) : w[i] for i in range( N )  }

		lp.set_mat_row( d + 1 , mapping )

		lp.set_row_bnds( d + 1 , None , W[d] )

	# a resource is used only once

	for i in range( N ) :

		mapping = { x( d , i ) : 1 for d in range( D ) }

		lp.set_mat_row( D + i + 1 , mapping )

		lp.set_row_bnds( D + i + 1 , None , 1 )

	lp.set_obj_dir( 'maximize' )

	return lp


def solve ( D , N , lp ) :

	x = lambda d , i  : d * N + i + 1

	# configure and solve

	iocp = glpk.IntOptControls() # (default) int. opt. control parameters
	iocp.presolve = True

	status = lp.intopt(iocp)

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	# fix the binary variable to its compute
	# value and find exact solution

	for d in range( D ) :

		for i in range( N ) :

			val = lp.mip_col_val( x( d , i ) )
			lp.set_col_bnds( x( d , i ) , val , val )

	smcp = glpk.SimplexControls( ) # (default) simplex control parameters
	smcp.presolve = True

	status = lp.simplex(smcp)  # solve

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	smcp.presolve = False
	status = lp.exact(smcp)  # now solve exactly

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	print( lp.get_obj_val( ) )


def solution ( D , N , lp ) :

	x = lambda d , i  : d * N + i + 1

	return ( lp.mip_col_val( x( d , i ) ) for d in range( D ) for i in range( N ) )
