
#include <iostream>
#include <fstream>
#include <limits>
#include <string>
#include <glpk.h>

static const char ON = '1' ;
static char* input ;
static char* output ;
static int D , N , R , P , LB , UB , C , skip ;
static double* SOL = NULL ;
static glp_prob* lp = NULL ;
static int* v = NULL ;
static int* w = NULL ;
static int* W = NULL ;
static int* LEN = NULL ;
static int** ROW = NULL ;

static int fp_heur ;
static int gmi_cuts ;
static int mir_cuts ;
static int cov_cuts ;
static int clq_cuts ;

typedef void (*cb)( glp_tree* , void* ) ;

static cb cb_func = NULL ;

static int tm_lim ;
static int fix_knapsack ;
static int fix_partition ;

void clean ( ) {

	delete[] SOL ;
	delete[] v ;
	delete[] w ;
	delete[] W ;
	delete[] LEN ;

	for ( int r = 0 ; r < R ; ++r ) {
		delete[] ROW[r] ;
	}

	delete[] ROW ;

	glp_delete_prob( lp ) ;

}

int Z ( ) {
	return 1 ;
}

int g ( int p ) {
	return ( Z( ) + 1 ) + p ;
}

int a ( int p ) {
	return g( P ) + p ;
}

int s ( int r , int p ) {
	return a( P ) + r * P + p ;
}

int x ( int d , int i , int p ) {
	return s( R , 0 ) + ( d * N + i ) * P + p ;
}

int columns ( ) {
	return x( D - 1 , N - 1 , P - 1 ) ;
}


void problem ( ) {

	lp = glp_create_prob( ) ;

	glp_add_cols( lp , C ) ;

	glp_add_rows( lp , ( D + N ) + ( P + R * P ) + ( P + R * P ) ) ;

	glp_set_obj_dir( lp , GLP_MAX ) ;

	glp_set_obj_coef( lp , Z( ) , 1 ) ;

	glp_set_col_bnds( lp , Z( ) , GLP_DB , LB , UB ) ;

	for ( int d = 0 ; d < D ; ++d ) {
		for ( int i = 0 ; i < N ; ++i ) {
			for ( int p = 0 ; p < P ; ++p ) {

				glp_set_col_kind( lp , x( d , i , p ) , GLP_BV ) ;

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

				ind[j] = x( d , i , p ) ;
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

				ind[j] = x( d , i , p ) ;
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

		ind[j] = a( p ) ;
		val[j] = -1 ;

		j += 1 ;

		for ( int d = 0 ; d < D ; ++d ) {
			for ( int i = 0 ; i < N ; ++i ) {

				ind[j] = x( d , i , p ) ;
				val[j] = v[i] ;

				j += 1 ;

			}
		}

		glp_set_mat_row( lp , k , len , ind , val ) ;

		delete[] ind ;
		delete[] val ;

		glp_set_row_bnds( lp , k , GLP_FX , 0 , 0 ) ;

		glp_set_col_bnds( lp , a( p ) , GLP_LO , 0 , -1 ) ;

		k += 1 ;

	}

	for ( int r = 0 ; r < R ; ++r ) {

		for ( int p = 0 ; p < P ; ++p ) {

			int len = 1 + LEN[r] * N ;
			int* ind = new int[len+1] ;
			double* val = new double[len+1] ;

			int j = 1 ;

			ind[j] = s( r , p ) ;
			val[j] = -1 ;

			j += 1 ;

			for ( int _d = 0 ; _d < LEN[r] ; ++_d ) {

				int d = ROW[r][_d] ;

				for ( int i = 0 ; i < N ; ++i ) {

					ind[j] = x( d , i , p ) ;
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

		ind[j] = Z( ) ;
		val[j] = -1 ;

		j += 1 ;

		ind[j] = g( p ) ;
		val[j] = 1 ;

		j += 1 ;

		glp_set_mat_row( lp , k , len , ind , val ) ;

		delete[] ind ;
		delete[] val ;

		glp_set_row_bnds( lp , k , GLP_LO , 0 , -1 ) ;

		glp_set_col_bnds( lp , g( p ) , GLP_LO , 0 , -1 ) ;

		k += 1 ;

	}


	for ( int r = 0 ; r < R ; ++r ) {

		for ( int p = 0 ; p < P ; ++p ) {

			int len = 1 + 1 + 1 ;
			int* ind = new int[len+1] ;
			double* val = new double[len+1] ;

			int j = 1 ;

			ind[j] = g( p ) ;
			val[j] = -1 ;

			j += 1 ;

			ind[j] = a( p ) ;
			val[j] = 1 ;

			j += 1 ;

			ind[j] = s( r , p ) ;
			val[j] = -1 ;

			j += 1 ;

			glp_set_mat_row( lp , k , len , ind , val ) ;

			delete[] ind ;
			delete[] val ;

			glp_set_row_bnds( lp , k , GLP_LO , 0 , -1 ) ;

			glp_set_col_bnds( lp , s( r , p ) , GLP_LO , 0 , -1 ) ;

			k += 1 ;

		}

	}

	if ( fix_knapsack == GLP_ON ) {

		for ( int i = 0 ; i < N ; ++i ) {
			for ( int d = 0 ; d < D ; ++d ) {
				for ( int p = 0 ; p < P ; ++p ) {

					int c = x( d , i , p ) ;

					if ( SOL[c] ) {

						for ( int _d = 0 ; _d < D ; ++_d ) {

							if ( _d == d ) continue ;

							for ( int _p = 0 ; _p < P ; ++_p ) {

								glp_set_col_bnds( lp , x( _d , i , _p ) , GLP_FX , 0 , 0 ) ;

							}

						}

						goto servers ;

					}
				}
			}

			// if we reach here then server is not used

			for ( int d = 0 ; d < D ; ++d ) {
				for ( int p = 0 ; p < P ; ++p ) {
					glp_set_col_bnds( lp , x( d , i , p ) , GLP_FX , 0 , 0 ) ;
				}
			}

			servers :;

		}
	}

	if ( fix_partition == GLP_ON ) {

		for ( int i = 0 ; i < N ; ++i ) {
			for ( int d = 0 ; d < D ; ++d ) {
				for ( int p = 0 ; p < P ; ++p ) {

					int c = x( d , i , p ) ;

					if ( SOL[c] ) {

						for ( int _d = 0 ; _d < D ; ++_d ) {

							for ( int _p = 0 ; _p < P ; ++_p ) {

								if ( _p == p ) continue ;

								glp_set_col_bnds( lp , x( _d , i , _p ) , GLP_FX , 0 , 0 ) ;

							}

						}

						goto servers2 ;

					}
				}
			}

			// if we reach here then server is not used

			for ( int d = 0 ; d < D ; ++d ) {
				for ( int p = 0 ; p < P ; ++p ) {
					glp_set_col_bnds( lp , x( d , i , p ) , GLP_FX , 0 , 0 ) ;
				}
			}

			servers2 :;

		}
	}
}

void solutionmip ( ) {

	for ( int c = 1 ; c <= C ; ++c ) {

		SOL[c] = glp_mip_col_val( lp , c ) ;

	}

}

void solution ( ) {

	for ( int c = 1 ; c <= C ; ++c ) {

		SOL[c] = glp_get_col_prim( lp , c ) ;

	}

}

void solve ( ) {

	glp_iocp iocp ;
	glp_init_iocp( &iocp ) ;
	iocp.presolve = true ;
	iocp.cb_func = cb_func ;
	iocp.fp_heur = fp_heur ;
	iocp.gmi_cuts = gmi_cuts ;
	iocp.mir_cuts = mir_cuts ;
	iocp.cov_cuts = cov_cuts ;
	iocp.clq_cuts = clq_cuts ;
	iocp.tm_lim = tm_lim ;

	int status ;

	status = glp_intopt( lp , &iocp ) ;

	if ( status != 0 ) {
		std::cout << "Error while solving...: " << status << std::endl ;
		exit( status ) ;
	}

	for ( int d = 0 ; d < D ; ++d ) {

		for ( int i = 0 ; i < N ; ++i ) {

			for ( int p = 0 ; p < P ; ++p ) {

				const int c = x( d , i , p ) ;

				double val = SOL[ c ] ;

				glp_set_col_bnds( lp , c , GLP_FX , val , val ) ;

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


void in ( ) {

	std::ifstream ifs ( input , std::ifstream::in ) ;

	ifs >> D >> N >> R >> P ;
	ifs >> skip ;
	if ( LB < 0 ) LB = skip ;
	ifs >> skip ;
	if ( UB < 0 ) UB = skip ;

	std::cout << D << " intervals" << std::endl ;
	std::cout << N << " servers" << std::endl ;
	std::cout << R << " rows" << std::endl ;
	std::cout << P << " groups" << std::endl ;
	std::cout << LB << " LB" << std::endl ;
	std::cout << UB << " UB" << std::endl ;

	C = columns( ) ;

	std::cout << C << " variables" << std::endl ;

	std::cout << "reading capacities and sizes" << std::endl ;

	v = new int[N] ;
	w = new int[N] ;

	for ( int i = 0 ; i < N ; ++i ) {
		ifs >> v[i] >> w[i] ;
	}

	std::cout << "reading size of knapsacks" << std::endl ;

	W = new int[D] ;

	for ( int d = 0 ; d < D ; ++d ) {
		ifs >> W[d] ;
	}

	LEN = new int[R] ;

	for ( int r = 0 ; r < R ; ++r ) {
		ifs >> LEN[r] ;
	}

	ROW = new int*[R] ;

	for ( int r = 0 ; r < R ; ++r ) {

		int _D = LEN[r] ;
		ROW[r] = new int[_D] ;

		for ( int _d = 0 ; _d < _D ; ++_d ) {
			ifs >> ROW[r][_d] ;
		}

	}

	SOL = new double[C + 1] ;

	for ( int c = 1 ; c <= C ; ++c ) {
		ifs >> SOL[c] ;
	}

	ifs.close( ) ;

}

void out ( ) {

	const int Z = SOL[1] ;

	const std::string postfix = "-" + std::to_string( Z ) ;

	const std::string name = output + postfix ;

	std::cout << "writing solution with objective value " << Z << " to " << name << std::endl ;

	std::ofstream ofs ( name , std::ofstream::out ) ;

	const char* n = "\n" ;

	ofs << D << n << N << n << R << n << P << n << LB << n << UB << n ;

	for ( int i = 0 ; i < N ; ++i ) {
		ofs << v[i] << n << w[i] << n ;
	}

	for ( int d = 0 ; d < D ; ++d ) {
		ofs << W[d] << n ;
	}

	for ( int r = 0 ; r < R ; ++r ) {
		ofs << LEN[r] << n ;
	}

	for ( int r = 0 ; r < R ; ++r ) {

		int _D = LEN[r] ;

		for ( int _d = 0 ; _d < _D ; ++_d ) {
			ofs << ROW[r][_d] << n ;
		}

	}

	for ( int c = 1 ; c <= C ; ++c ) {
		ofs << SOL[c] << n ;
	}

	ofs.close( ) ;

}

void refresh ( glp_tree* tree , void* ) {

	if ( glp_ios_reason( tree ) == GLP_IHEUR ) {

		std::cout << "loading existing solution" << std::endl ;

		if ( glp_ios_heur_sol( tree , SOL ) == 0 ) {

			std::cout << "existing solution accepted" << std::endl ;

		}

		else {

			std::cout << "existing solution rejected" << std::endl ;

		}

	}

	else if ( glp_ios_reason( tree ) == GLP_IBINGO ) {

		solutionmip( ) ;
		out( ) ;

	}

}

void load ( glp_tree* tree , void* ) {

	if ( glp_ios_reason( tree ) == GLP_IHEUR && glp_ios_curr_node( tree ) == 1 ) {

		std::cout << "loading existing solution" << std::endl ;

		if ( glp_ios_heur_sol( tree , SOL ) == 0 ) {

			std::cout << "existing solution accepted" << std::endl ;

		}

		else {

			std::cout << "existing solution rejected" << std::endl ;

		}

	}

	else if ( glp_ios_reason( tree ) == GLP_IBINGO ) {

		solutionmip( ) ;
		out( ) ;

	}

}
int flag ( char* arg ) {

	return arg[0] == ON ? GLP_ON : GLP_OFF ;

}

int main ( int argc , char** argv ) {

	if ( argc < 14 ) {
		std::cout << "(01) <input>" << std::endl ;
		std::cout << "(02) <output>" << std::endl ;
		std::cout << "(03) <fp_heur>" << std::endl ;
		std::cout << "(04) <gmi_cuts>" << std::endl ;
		std::cout << "(05) <mir_cuts>" << std::endl ;
		std::cout << "(06) <cov_cuts>" << std::endl ;
		std::cout << "(07) <clq_cuts>" << std::endl ;
		std::cout << "(08) <cb_func>" << std::endl ;
		std::cout << "(09) <tm_lim>" << std::endl ;
		std::cout << "(10) <LB>" << std::endl ;
		std::cout << "(11) <UB>" << std::endl ;
		std::cout << "(12) <fix_knapsack>" << std::endl ;
		std::cout << "(13) <fix_partition>" << std::endl ;
		exit( -1 ) ;
	}

	input = argv[1] ;
	output = argv[2] ;

	fp_heur = flag( argv[3] ) ;
	gmi_cuts = flag( argv[4] ) ;
	mir_cuts = flag( argv[5] ) ;
	cov_cuts = flag( argv[6] ) ;
	clq_cuts = flag( argv[7] ) ;
	cb_func = argv[8][0] == ON ? refresh : load ;

	tm_lim = std::stoi( argv[9] ) ;
	if ( tm_lim < 0 ) tm_lim = std::numeric_limits<int>::max( ) ;

	LB = std::stoi( argv[10] ) ;
	UB = std::stoi( argv[11] ) ;
	fix_knapsack = flag( argv[12] ) ;
	fix_partition = flag( argv[13] ) ;

	std::cout << "<input> " << input << std::endl ;
	std::cout << "<output> " << output << std::endl ;
	std::cout << "<fp_heur> " << fp_heur << std::endl ;
	std::cout << "<gmi_cuts> " << gmi_cuts << std::endl ;
	std::cout << "<mir_cuts> " << mir_cuts << std::endl ;
	std::cout << "<cov_cuts> " << cov_cuts << std::endl ;
	std::cout << "<clq_cuts> " << clq_cuts << std::endl ;
	std::cout << "<cb_func> " << ( cb_func == load ? "load" : "refresh" ) << std::endl ;
	std::cout << "<tm_lim> " << tm_lim << std::endl ;
	std::cout << "<fix_knapsack> " << fix_knapsack << std::endl ;
	std::cout << "<fix_partition> " << fix_partition << std::endl ;

	std::cout << "reading input" << std::endl ;
	in( ) ;
	std::cout << "building problem" << std::endl ;
	problem( ) ;
	std::cout << "solving problem" << std::endl ;
	solve( ) ;
	std::cout << "extract solution" << std::endl ;
	solution( ) ;
	std::cout << "write output" << std::endl ;
	out( ) ;
	std::cout << "clean up" << std::endl ;
	clean( ) ;

}
