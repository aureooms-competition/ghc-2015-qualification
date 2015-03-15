
#include <glpk.h>

class Variables {

public:

	const int D ;
	const int N ;
	const int R ;
	const int P ;

	Variables ( const int D , const int N , const int R , const int P ) : D(D) , N(N) , R(R) , P(P) { }

	int Z ( ) {
		return 1 ;
	}

	int g ( int p ) {
		return ( this->Z( ) + 1 ) + p ;
	}

	int a ( int p ) {
		return this->g( this->P ) + p ;
	}

	int s ( int r , int p ) {
		return this->a( this->P ) + r * this->P + p ;
	}

	int x ( int d , int i , int p ) {
		return this->s( this->R , 0 ) + ( d * this->N + i ) * this->P + p ;
	}

	int size ( ) {
		return this->x( this->D - 1 , this->N - 1 , this->P - 1 ) ;
	}

} ;

glp_prob* problem ( const int D , const int N , const int R , const int P , int[] v , int[] w , int[] W , int[] LEN , int[][] ROW , int lb , int ub ) {

	Variables var ( D , N , R , P ) ;

	glp_prob* lp = glp_create_prob( ) ;

	glp_add_cols( lp , var.size( ) ) ;

	glp_add_rows( lp , ( D + N ) + ( P + R * P ) + ( P + R * P ) ) ;

	glp_set_obj_dir( lp , GLP_MAX ) ;

	glp_set_obj_coef( lp , var.Z( ) , 1 ) ;

	glp_set_col_bnds( lp , var.Z( ) , GLP_DB , lb , up ) ;

	for ( int d = 0 ; d < D ; ++d ) {
		for ( int i = 0 ; i < N ; ++i ) {
			for ( int p = 0 ; p < P ; ++p ) {

				glp_set_col_kind( lp , var.x( d , i , p ) , GLP_BV ) ;

			}
		}
	}


	int k = 1 ;

	for ( int d = 0 ; d < D ; ++d ) {

		int len = N * P ;
		int ind[] = new int[len+1] ;
		double val[] = new double[len+1] ;

		int j = 1 ;

		for ( int i = 0 ; i < N ; ++i ) {
			for ( int p = 0 ; p < P ; ++p ) {

				ind[j] = var.x( d , i , p ) ;
				val[j] = w[i] ;

				j += 1 ;

			}
		}

		glp_set_mat_row( lp , k , len , ind , val ) ;

		delete[] ind ;
		delete[] val ;

		glp_set_row_bnds( lp , k , GLP_UB , -1 , W[d] ) ;

		k += 1 ;

	}

	for ( int i = 0 ; i < N ; ++i ) {

		int len = D * P ;
		int ind[] = new int[len+1] ;
		double val[] = new double[len+1] ;

		int j = 1 ;

		for ( int d = 0 ; d < D ; ++d ) {
			for ( int p = 0 ; p < P ; ++p ) {

				ind[j] = var.x( d , i , p ) ;
				val[j] = 1 ;

				j += 1 ;

			}
		}

		glp_set_mat_row( lp , k , len , ind , val ) ;

		delete[] ind ;
		delete[] val ;

		glp_set_row_bnds( lp , k , GLP_UB , -1 , 1 ) ;

		k += 1 ;

	}

	for ( int p = 0 ; p < P ; ++p ) {

		int len = 1 + D * N ;
		int ind[] = new int[len+1] ;
		double val[] = new double[len+1] ;

		int j = 1 ;

		ind[j] = var.a( p ) ;
		val[j] = -1 ;

		j += 1 ;

		for ( int d = 0 ; d < D ; ++d ) {
			for ( int i = 0 ; i < N ; ++i ) {

				ind[j] = var.x( d , i , p ) ;
				val[j] = v[i] ;

				j += 1 ;

			}
		}

		glp_set_mat_row( lp , k , len , ind , val ) ;

		delete[] ind ;
		delete[] val ;

		glp_set_row_bnds( lp , k , GLP_FX , 0 , 0 ) ;

		glp_set_col_bnds( lp , var.a( p ) , GLP_LO , 0 , -1 ) ;

		k += 1 ;

	}

	for ( int r = 0 ; r < R ; ++r ) {

		for ( int p = 0 ; p < P ; ++p ) {

			int len = 1 + LEN[r] * N ;
			int ind[] = new int[len+1] ;
			double val[] = new double[len+1] ;

			int j = 1 ;

			ind[j] = var.s( r , p ) ;
			val[j] = -1 ;

			j += 1 ;

			for ( int _d = 0 ; _d < LEN[r] ; ++_d ) {

				int _d = ROW[r][_d] ;

				for ( int i = 0 ; i < N ; ++i ) {

					ind[j] = var.x( d , i , p ) ;
					val[j] = v[i] ;

					j += 1 ;

				}
			}


			glp_set_mat_row( lp , k , len , ind , val ) ;

			delete[] ind ;
			delete[] val ;

			glp_set_row_bnds( lp , k , GLP_FX , 0 , 0 ) ;

			k += 1 ;

		}

	}


	for ( int p = 0 ; p < P ; ++p ) {

		int len = 1 + 1 ;
		int ind[] = new int[len+1] ;
		double val[] = new double[len+1] ;

		int j = 1 ;

		ind[j] = var.Z( ) ;
		val[j] = -1 ;

		j += 1 ;

		ind[j] = var.g( p ) ;
		val[j] = 1 ;

		j += 1 ;

		glp_set_mat_row( lp , k , len , ind , val ) ;

		delete[] ind ;
		delete[] val ;

		glp_set_row_bnds( lp , k , GLP_LB , 0 , -1 ) ;

		glp_set_col_bnds( lp , var.g( p ) , GLP_LB , 0 , -1 ) ;

		k += 1 ;

	}


	for ( int r = 0 ; r < R ; ++r ) :

		for ( int p = 0 ; p < P ; ++p ) {

			int len = 1 + 1 + 1 ;
			int ind[] = new int[len+1] ;
			double val[] = new double[len+1] ;

			int j = 1 ;

			ind[j] = var.g( p ) ;
			val[j] = -1 ;

			j += 1 ;

			ind[j] = var.a( p ) ;
			val[j] = 1 ;

			j += 1 ;

			ind[j] = var.s( r , p ) ;
			val[j] = -1 ;

			j += 1 ;

			glp_set_mat_row( lp , k , len , ind , val ) ;

			delete[] ind ;
			delete[] val ;

			glp_set_row_bnds( lp , k , GLP_LO , 0 , -1 ) ;

			glp_set_col_bnds( lp , var.s( r , p ) , GLP_LO , 0 , -1 ) ;

			k += 1 ;

		}

	}

	return lp ;

}

def load ( D , N , R , P , lp , SRV ) :

	var = Variables( D , N , R , P )

	def cb ( tree , info ) :

		if tree.ios_reason( ) == GLP_IHEUR and tree.ios_curr_node( ) == 1 :

			tree.ios_heur_sol( { var.x( d , i , p ) : 0 if SRV[i] is None or SRV[i][0] != d or SRV[i][1] != p else 1 for d in range( D ) for i in range( N ) for p in range( P ) } )

	return cb

def solve ( D , N , R , P , lp , cb = None ) :

	var = Variables( D , N , R , P )

	# configure and solve

	iocp = glpk.IntOptControls() # (default) int. opt. control parameters
	iocp.presolve = True

	if cb : iocp.cb_func = cb

	status = glp_intopt(iocp)

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	# fix the binary variable to its compute
	# value and find exact solution

	for d in range( D ) :

		for i in range( N ) :

			for ( int p = 0 ; p < P ; ++p ) {

				val = glp_mip_col_val( var.x( d , i , p ) )

				glp_set_col_bnds( var.x( d , i , p ) , val , val )

	smcp = glpk.SimplexControls( ) # (default) simplex control parameters
	smcp.presolve = True

	status = glp_simplex(smcp)  # solve

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	smcp.presolve = False
	status = glp_exact(smcp)  # now solve exactly

	if status != 'optimal' :
		raise RuntimeError( 'Error while solving...: ' + status )

	print( glp_get_obj_val( ) )


def solution ( D , N , R , P , lp ) :

	var = Variables( D , N , R , P )

	return ( glp_mip_col_val( var.x( d , i , p ) ) for d in range( D ) for i in range( N ) for p in range( P ) )
