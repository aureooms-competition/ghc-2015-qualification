
#include "pfsp_commons/framework.hpp"

#include "pfsp_vnd/global.hpp"
#include "pfsp_vnd/config.hpp"


using namespace pfsp_vnd;


void run(){

// PARSE INPUT

	pfsp::framework::parse(global::params[0], global::i);

	if(global::verbose){
		std::cout << "jobs " << global::i.nbJob << std::endl;
		std::cout << "mach " << global::i.nbMac << std::endl;
	}


// INIT EVAL

	pfsp::framework::init_eval<I,E,TE,IE,EE>(global::i, global::e, global::transpose.eval, global::insert.eval, global::exchange.eval);

	global::stranspose.eval = global::transpose.eval;
	global::sinsert.eval = global::insert.eval;
	global::sexchange.eval = global::exchange.eval;


// SOLUTION

	S s(global::i.nbJob + 1);


// GEN INITIAL SOLUTION

	auto init = global::init[global::INIT];
	(*init)(s);
	val_t opt = (*global::e)(s);

	// PRINT IT
	if(global::verbose){
		std::cout << "init ";
		lib::io::format(std::cout, s, global::list_p) << std::endl;
		std::cout << opt << std::endl;
	}


// ALIAS

	auto ordering = global::ordering[global::ORDERING];
	auto pivoting = global::pivoting[global::PIVOTING];

// FIND LOCAL OPTIMUM

	hrclock::time_point beg = hrclock::now();


	// VND ALGORITHM
	size_t k = 0;

	while(k < ordering.size()){
		R best = pivoting(s, ordering[k]->walk, ordering[k]->eval);
		while(best.first){
			opt += best.first;
			(*ordering[k]->eval)(s, best.second, global::e->detail, global::e->wt);
			(*ordering[k]->apply)(s, best.second);

			if(global::verbose){
				++global::steps;
				pfsp::framework::print_step(std::cout, global::steps, hrclock::now() - beg, opt);
			}

			k = 0;
			best = pivoting(s, ordering[k]->walk, ordering[k]->eval);
		}
		++k;
	}
	// <end>
	
	hrclock::time_point end  = hrclock::now();


// CLEAN

	pfsp::framework::clean_eval(global::e, global::transpose.eval, global::insert.eval, global::exchange.eval);


// OUTPUT

	pfsp::framework::output(std::cout, global::verbose, s, global::list_p, opt, end - beg, global::seed_v);
}


int main(int argc, char *argv[]){
	return pfsp::framework::main(std::cout, argc, argv, global::help, &config::fill, &config::help, &config::check, &run);
}
