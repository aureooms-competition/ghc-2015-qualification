
import ecyglpki as glpk

def test1 ( ) :

	# set up the problem
	lp = glpk.Problem()

	# max z = 5 x + 4 y
	# s.t.    6 x + 4 y <= 24 (1)
	#         1 x + 2 y <=  6 (2)
	#         0 x + 1 y <=  2 (3)
	#        -1 x + 1 y <=  1 (4)
	#           x       >=  0
	#                 y >=  0

	lp.add_named_rows( '(1)' , '(2)' , '(3)' , '(4)' )

	lp.set_row_bnds( '(1)' , None , 24 )
	lp.set_row_bnds( '(2)' , None ,  6 )
	lp.set_row_bnds( '(3)' , None ,  2 )
	lp.set_row_bnds( '(4)' , None ,  1 )

	lp.add_named_cols( 'x' , 'y' )

	lp.set_obj_coef( 'x' ,  5 )
	lp.set_obj_coef( 'y' ,  4 )

	lp.set_col_bnds( 'x' , 0 , None )
	lp.set_col_bnds( 'y' , 0 , None )

	lp.set_mat_col( 'x' , { '(1)' : 6 , '(2)' : 1 , '(3)' : 0 , '(4)' : -1 } )
	lp.set_mat_col( 'y' , { '(1)' : 4 , '(2)' : 2 , '(3)' : 1 , '(4)' :  1 } )

	lp.set_obj_dir( 'maximize' )

	# configure and solve

	iocp = glpk.IntOptControls() # (default) int. opt. control parameters
	iocp.presolve = True

	status = lp.intopt(iocp)

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	smcp = glpk.SimplexControls( ) # (default) simplex control parameters
	smcp.presolve = True

	status = lp.simplex(smcp)  # solve

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	smcp.presolve = False
	status = lp.exact(smcp)  # now solve exactly

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	print( 'x = %s' % lp.mip_col_val( 'x' ) )
	print( 'y = %s' % lp.mip_col_val( 'y' ) )


def test2 ( ) :

	# set up the problem
	lp = glpk.Problem()

	# max z = 5 x + 4 y
	# s.t.    6 x + 4 y <= 24 (1)
	#         1 x + 2 y <=  6 (2)
	#        -1 x + 1 y <=  1 (3)
	#           x       >=  0
	#                 y is  0 or 1

	lp.add_named_rows( '(1)' , '(2)' , '(3)' )

	lp.set_row_bnds( '(1)' , None , 24 )
	lp.set_row_bnds( '(2)' , None ,  6 )
	lp.set_row_bnds( '(3)' , None ,  1 )

	lp.add_named_cols( 'x' , 'y' )

	lp.set_obj_coef( 'x' ,  5 )
	lp.set_obj_coef( 'y' ,  4 )

	lp.set_col_bnds( 'x' , 0 , None )
	lp.set_col_kind( 'y' , 'binary' )

	lp.set_mat_col( 'x' , { '(1)' : 6 , '(2)' : 1 , '(3)' : -1 } )
	lp.set_mat_col( 'y' , { '(1)' : 4 , '(2)' : 2 , '(3)' :  1 } )

	lp.set_obj_dir( 'maximize' )


	# configure and solve

	iocp = glpk.IntOptControls() # (default) int. opt. control parameters
	iocp.presolve = True

	status = lp.intopt(iocp)

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	# fix the binary variable to its compute
	# value and find exact solution

	val = lp.mip_col_val( 'y' )
	lp.set_col_bnds( 'y' , val , val )

	smcp = glpk.SimplexControls( ) # (default) simplex control parameters
	smcp.presolve = True

	status = lp.simplex(smcp)  # solve

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	smcp.presolve = False
	status = lp.exact(smcp)  # now solve exactly

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	print( 'x = %s' % lp.mip_col_val( 'x' ) )
	print( 'y = %s' % lp.mip_col_val( 'y' ) )
