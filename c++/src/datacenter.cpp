
#include <iostream>
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

glp_prob* problem ( const int D , const int N , const int R , const int P , int* v , int* w , int* W , int* LEN , int** ROW , int lb , int ub ) {

	Variables var ( D , N , R , P ) ;

	glp_prob* lp = glp_create_prob( ) ;

	glp_add_cols( lp , var.size( ) ) ;

	glp_add_rows( lp , ( D + N ) + ( P + R * P ) + ( P + R * P ) ) ;

	glp_set_obj_dir( lp , GLP_MAX ) ;

	glp_set_obj_coef( lp , var.Z( ) , 1 ) ;

	glp_set_col_bnds( lp , var.Z( ) , GLP_DB , lb , ub ) ;

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
		int* ind = new int[len+1] ;
		double* val = new double[len+1] ;

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

		glp_set_row_bnds( lp , k , GLP_UP , -1 , W[d] ) ;

		k += 1 ;

	}

	for ( int i = 0 ; i < N ; ++i ) {

		int len = D * P ;
		int* ind = new int[len+1] ;
		double* val = new double[len+1] ;

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

		glp_set_row_bnds( lp , k , GLP_UP , -1 , 1 ) ;

		k += 1 ;

	}

	for ( int p = 0 ; p < P ; ++p ) {

		int len = 1 + D * N ;
		int* ind = new int[len+1] ;
		double* val = new double[len+1] ;

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
			int* ind = new int[len+1] ;
			double* val = new double[len+1] ;

			int j = 1 ;

			ind[j] = var.s( r , p ) ;
			val[j] = -1 ;

			j += 1 ;

			for ( int _d = 0 ; _d < LEN[r] ; ++_d ) {

				int d = ROW[r][_d] ;

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
		int* ind = new int[len+1] ;
		double* val = new double[len+1] ;

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

		glp_set_row_bnds( lp , k , GLP_LO , 0 , -1 ) ;

		glp_set_col_bnds( lp , var.g( p ) , GLP_LO , 0 , -1 ) ;

		k += 1 ;

	}


	for ( int r = 0 ; r < R ; ++r ) {

		for ( int p = 0 ; p < P ; ++p ) {

			int len = 1 + 1 + 1 ;
			int* ind = new int[len+1] ;
			double* val = new double[len+1] ;

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

static double* SOL = NULL;

void load ( glp_tree* tree , void* info ) {

	if ( glp_ios_reason( tree ) == GLP_IHEUR && glp_ios_curr_node( tree ) == 1 ) {

		glp_ios_heur_sol( tree , SOL ) ;

	}

}


void solve ( const int D , const int N , const int R , const int P , glp_prob* lp ) {

	Variables var ( D , N , R , P ) ;

	glp_iocp iocp ;
	glp_init_iocp( &iocp ) ;
	iocp.presolve = true ;
	iocp.cb_func = load ;

	int status ;

	status = glp_intopt( lp , &iocp ) ;

	if ( status != 0 ) {
		std::cout << "Error while solving...: " << status << std::endl ;
		exit( status ) ;
	}

	for ( int d = 0 ; d < D ; ++d ) {

		for ( int i = 0 ; i < N ; ++i ) {

			for ( int p = 0 ; p < P ; ++p ) {

				double val = glp_mip_col_val( lp , var.x( d , i , p ) ) ;

				glp_set_col_bnds( lp , var.x( d , i , p ) , GLP_FX , val , val ) ;

			}
		}
	}

	glp_smcp smcp ;
	glp_init_smcp( &smcp ) ;
	smcp.presolve = true ;

	status = glp_simplex( lp , &smcp ) ;

	if ( status != 0 ) {
		std::cout << "Error while solving...: " << status << std::endl ;
		exit( status ) ;
	}

	smcp.presolve = false ;
	status = glp_exact( lp , &smcp ) ;

	if ( status != 0 ) {
		std::cout << "Error while solving...: " << status << std::endl ;
		exit( status ) ;
	}

	 std::cout << glp_get_obj_val( lp ) << std::endl ;

}

int main ( int argc , char** argv ) {

	std::cout << "Hello, world!" << std::endl ;

}
