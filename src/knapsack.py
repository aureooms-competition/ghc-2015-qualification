
import ecyglpki as glpk

def multidimensional ( D , N , v , w , W ) :

	lp = glpk.Problem()

	lp.add_rows( D )

	for d in range( D ) :

		lp.set_row_bnds( d + 1 , None , W[d] )

	lp.add_cols( N * D )

	for d in range( D ) :

		for i in range( N ) :

			x = d * N + i + 1

			lp.set_obj_coef( x , v[i] )
			lp.set_col_kind( x , 'binary' )

			lp.set_mat_col( x , { d + 1 : w[i] for d in range( D ) } )

	lp.set_obj_dir( 'maximize' )

	return lp


def solve ( D , N , lp ) :

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

			x = d * N + i + 1

			val = lp.mip_col_val( x )
			lp.set_col_bnds( x , val , val )

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
