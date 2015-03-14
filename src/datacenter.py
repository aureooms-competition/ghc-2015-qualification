
try :

	GLP_IHEUR = 0x03

	import ecyglpki as glpk

	import itertools

	class Variables ( object ) :

		def __init__ ( self , D , N , R , P ) :

			self.D = D
			self.N = N
			self.R = R
			self.P = P

		def Z ( self ) :

			return 1

		def g ( self , p ) :

			return ( self.Z( ) + 1 ) + p

		def a ( self , p ) :

			return self.g( self.P ) + p

		def s ( self , r , p ) :

			return self.a( self.P ) + r * self.P + p

		def x ( self , d , i , p ) :

			return self.s( self.R , 0 ) + ( d * self.N + i ) * self.P + p

		def __len__ ( self ) :

			return self.x( self.D - 1 , self.N - 1 , self.P - 1 )

	def problem ( D , N , R , P , v , w , W , ROW , lb = 0 , ub = None ) :

		var = Variables( D , N , R , P )

		lp = glpk.Problem( )

		lp.add_cols( len( var ) )

		lp.add_rows( ( D + N ) + ( P + R * P ) + ( P + R * P ) )

		lp.set_obj_dir( 'maximize' )

		lp.set_obj_coef( var.Z( ) , 1 )

		lp.set_col_bnds( var.Z( ) , lb , ub )

		for d in range( D ) :

			for i in range( N ) :

				for p in range( P ) :

					lp.set_col_kind( var.x( d , i , p ) , "binary" )

		k = 1

		for d in range( D ) :

			mapping = { var.x( d , i , p ) : w[i] for i in range( N ) for p in range( P )  }

			lp.set_mat_row( k , mapping )

			lp.set_row_bnds( k , None , W[d] )

			k += 1

		for i in range( N ) :

			mapping = { var.x( d , i , p ) : 1 for d in range( D ) for p in range( P ) }

			lp.set_mat_row( k , mapping )

			lp.set_row_bnds( k , None , 1 )

			k += 1

		for p in range( P ) :

			a = ( ( var.a( p ) , -1 ) , )
			x = ( ( var.x( d , i , p ) , v[i] ) for d in range( D ) for i in range( N ) )

			mapping = { V : C for V , C in itertools.chain( a , x ) }

			lp.set_mat_row( k , mapping )

			lp.set_row_bnds( k , 0 , 0 )

			lp.set_col_bnds( var.a( p ) , 0 , None )

			k += 1

		for r in range( R ) :

			for p in range( P ) :

				s = ( ( var.s( r , p ) , -1 ) , )
				x = ( ( var.x( d , i , p ) , v[i] ) for d in ROW[r] for i in range( N ) )

				mapping = { V : C for V , C in itertools.chain( s , x ) }

				lp.set_mat_row( k , mapping )

				lp.set_row_bnds( k , 0 , 0 )

				k += 1


		for p in range( P ) :

			K = ( ( var.Z( ) , -1 ) , ( var.g( p ) , 1 ) )

			mapping = { V : C for V , C in K }

			lp.set_mat_row( k , mapping )

			lp.set_row_bnds( k , 0 , None )

			lp.set_col_bnds( var.g( p ) , 0 , None )

			k += 1


		for r in range( R ) :

			for p in range( P ) :

				K = ( ( var.g( p ) , -1 ) , ( var.a( p ) , 1 ) , ( var.s( r , p ) , -1 ) )

				mapping = { V : C for V , C in K }

				lp.set_mat_row( k , mapping )

				lp.set_row_bnds( k , 0 , None )

				lp.set_col_bnds( var.s( r , p ) , 0 , None )

				k += 1


		return lp


	def load ( D , N , R , P , lp , SRV ) :

		var = Variables( D , N , R , P )

		def cb ( tree , info ) :

			if tree.ios_reason( ) == GLP_IHEUR and tree.ios_curr_node( ) == 1 :

				tree.ios_heur_sol( { var.x( d , i , p ) : 0 if SRV[i] is None or SRV[i][0] != d or SRV[i][1] != p else 1 for d in range( D ) for i in range( N ) for p in range( P ) } )

	def solve ( D , N , R , P , lp , cb = None ) :

		var = Variables( D , N , R , P )

		# configure and solve

		iocp = glpk.IntOptControls() # (default) int. opt. control parameters
		iocp.presolve = True

		if cb : iocp.cb_func = cb

		status = lp.intopt(iocp)

		if status != 'optimal' :
			raise RuntimeError( 'Error while solving...: ' + status )

		# fix the binary variable to its compute
		# value and find exact solution

		for d in range( D ) :

			for i in range( N ) :

				for p in range( P ) :

					val = lp.mip_col_val( var.x( d , i , p ) )

					lp.set_col_bnds( var.x( d , i , p ) , val , val )

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


	def solution ( D , N , R , P , lp ) :

		var = Variables( D , N , R , P )

		return ( lp.mip_col_val( var.x( d , i , p ) ) for d in range( D ) for i in range( N ) for p in range( P ) )

except ImportError as e :

	_e = e

	def notify ( *args , **kwargs ) : raise _e

	knapsack = solver = solution = load = notify

