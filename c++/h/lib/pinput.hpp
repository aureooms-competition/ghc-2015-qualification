#ifndef _LIB_PINPUT_HPP
#define _LIB_PINPUT_HPP

#include <string>
#include <utility>
#include <locale>


// HELPER

#include <vector>
#include <tuple>
#include <set>
#include <map>
#include <iostream>
#include <sstream>
#include "lib/error/exception.hpp"
#include "lib/io.hpp"


namespace lib{
namespace pinput{


/**
 * Function template for command line arguments parsing.
 * 
 * @author Ooms Aurélien
 * 
 * @param <P> out param array type
 * @param <O> out option map type
 * @param <F> out flag set type
 * @param <T> option set type
 * @param <U> flag set type
 * 
 * @param argc argv size
 * @param argv argument vector
 * @param params out param array
 * @param options out option map
 * @param flags out flag set
 * @param option_set option set
 * @param flag_set flag set
 *
 */

template<typename P, typename O, typename F, typename T, typename U>
void parse(int argc, char* argv[], P& params, O& options, F& flags, const T& option_set, const U& flag_set){

	std::string optionalParameterKey;
	bool isOptionalParameter = false;

	for(int n = 1; n < argc; ++n){
		std::string p = argv[n];
		if (p[0] == '-' && !std::isdigit(p[1])){
			isOptionalParameter = false;
			if(p.size() > 1){
				if(p[1] == '-' || p.size() == 2){

					if(option_set.count(p) > 0){
						options.insert(typename O::value_type(p, {}));
						optionalParameterKey = p;
						isOptionalParameter = true;
					}
					else if(flag_set.count(p) > 0){
						flags.insert(p);
					}
				}
				else{
					for(size_t i = 1; i < p.size(); ++i){
						flags.insert(std::string({'-', p[i]}));
					}
				}
			}
		}
		else if(isOptionalParameter){
			options.at(optionalParameterKey).push_back(p);
		}
		else{
			params.push_back(p);
		}
	}
}

/**
 * Helper for input parsing.
 */

class helper{

public:

	// CONDITIONS

	typedef bool(*C)();

	typedef struct{
		std::string key;
		C pred;
		std::string msg;
	} condition_t;

	std::vector<condition_t> oconditions, fconditions;

	helper& condition(const std::string& key, C pred, const std::string& msg){
		if(voptions.count(key)) oconditions.push_back(condition_t({key, pred, msg}));
		else if(vflags.count(key)) fconditions.push_back(condition_t({key, pred, msg}));
		else throw lib::error::exception("condition : '" + key + "' is neither option nor flag");
		return *this;
	}

	// MANDATORY

	std::vector<std::vector<std::vector<std::string>>> omandatory;

	helper& mandatory(const std::string& key){
		return mandatory(std::vector<std::string>(1, key));
	}

	helper& mandatory(const std::vector<std::string>& conjunction){
		return mandatory(std::vector<std::vector<std::string>>(1, conjunction));
	}

	helper& mandatory(const std::vector<std::vector<std::string>>& disjunction){

		for(const auto& c : disjunction){
			for(const auto& k : c){
				if(!voptions.count(k))
					throw lib::error::exception("mandatory : '" + k + "' is not an option");
			}
		}
		omandatory.push_back(disjunction);
		return *this;
	}

	// SIGNATURE
	
	typedef std::pair<std::string, std::string> signature_t;
	std::vector<signature_t> osignatures, fsignatures;

	helper& signature(){

		if(usage_msg.size() > 0){
			std::cout << "Usage: " << usage_msg << std::endl;
		}


		typedef std::vector<std::string> component_t;
		typedef struct{
			component_t names;
			std::string desc;
			component_t cond;
			component_t odefault;
			int omandatory = 0;
		} components_t;

		typedef std::pair<std::string, components_t> item_t;
		std::map<std::string, components_t> otext, ftext;
	
		if(options.size()){

			std::cout << "Options:" << std::endl;

			for(const auto& k : voptions){
				otext.insert(item_t(k, components_t()));
			}

			for(const auto& k : oaliases){
				otext.at(k.first).names.push_back(k.second);
			}

			for(const auto& k : osignatures){
				otext.at(k.first).desc = k.second;
			}

			for(const auto& k : oconditions){
				otext.at(k.key).cond.push_back(k.msg);
			}

			for(const auto& k : odefaults){
				otext.at(k.first).odefault = k.second;
			}

			for(const auto& d : omandatory){
				if(d.size() == 1 && d[0].size() == 1)
					otext.at(d[0][0]).omandatory = 1;
				else{
					for(const auto& c : d){
						for(const auto& v : c){
							if(!otext.at(v).omandatory)
								otext.at(v).omandatory = -1;
						}
					}
				}
			}

			for(const auto& component : otext){
				std::cout << "  " << component.first;
				if(component.second.omandatory == 1) std::cout << '*';
				else if(component.second.omandatory == -1) std::cout << '^';
				if(component.second.names.size()){
					std::cout << ' ';
					std::cout << component.second.names;
				}

				std::cout << " : " << component.second.desc;

				if(component.second.cond.size()){
					std::cout << " @condition ";
					std::cout << component.second.cond;
				}

				if(component.second.odefault.size()){
					std::cout << " @default ";
					std::cout << component.second.odefault;
				}

				std::cout << std::endl;
			}
		}
		if(flags.size()){
			std::cout << "Flags:" << std::endl;

			for(const auto& k : vflags){
				ftext.insert(item_t(k, components_t()));
			}

			for(const auto& k : faliases){
				ftext.at(k.first).names.push_back(k.second);
			}

			for(const auto& k : fsignatures){
				ftext.at(k.first).desc = k.second;
			}

			for(const auto& k : fconditions){
				ftext.at(k.key).cond.push_back(k.msg);
			}

			for(const auto& component : ftext){
				std::cout << "  " << component.first;
				if(component.second.names.size()){
					std::cout << ' ';
					std::cout << component.second.names;
				}

				std::cout << " : " << component.second.desc;

				if(component.second.cond.size()){
					std::cout << " @condition ";
					std::cout << component.second.cond;
				}

				std::cout << std::endl;
			}
		}



		return *this;
	}


	// OPTIONS

	std::set<std::string> options;
	std::set<std::string> voptions;

	helper& option(const std::string& key, const std::string& sign){
		if(flags.count(key)) throw lib::error::exception("option : '" + key + "' is a flag");
		osignatures.push_back(signature_t(key, sign));
		options.insert(key);
		voptions.insert(key);
		return *this;
	}


	// FLAGS

	std::set<std::string> flags;
	std::set<std::string> vflags;

	helper& flag(const std::string& key, const std::string& sign){
		if(options.count(key)) throw lib::error::exception("flag : '" + key + "' is an option");
		fsignatures.push_back(signature_t(key, sign));
		flags.insert(key);
		vflags.insert(key);
		return *this;
	}


	// ALIASES

	typedef std::pair<std::string, std::string> alias_t;

	std::vector<alias_t> oaliases, faliases;

	helper& alias(const std::string& key, const std::string& alias){

		if(options.count(alias))
			throw lib::error::exception("alias : '" + alias + "' is an option");
		else if(flags.count(alias))
			throw lib::error::exception("alias : '" + alias + "' is is a flag");
		else if(options.count(key)){
			options.insert(alias);
			oaliases.push_back(alias_t(key, alias));
		}
		else if(flags.count(key)){
			flags.insert(alias);
			faliases.push_back(alias_t(key, alias));
		}
		else throw lib::error::exception("alias : '" + key + "' is neither option nor flag");

		return *this;
	}

	// DEFAULTS

	typedef std::pair<std::string, std::vector<std::string>> default_t;

	std::vector<default_t> odefaults;

	helper& odefault(const std::string& key, const std::vector<std::string>& val){
		if(voptions.count(key)) odefaults.push_back(default_t(key, val));
		else throw lib::error::exception("default : '" + key + "' is not an option");
		return *this;
	}


	// ASSIGN
	typedef void(*A)(const std::vector<std::string>&);
	typedef void(*B)(const bool);

	typedef struct{
		std::string key;
		A fn;
	} oassign_t;

	typedef struct{
		std::string key;
		B fn;
	} fassign_t;

	std::vector<oassign_t> oassigns;
	std::vector<fassign_t> fassigns;

	helper& oassign(const std::string& key, A fn){
		if(voptions.count(key)) oassigns.push_back(oassign_t({key, fn}));
		else throw lib::error::exception("assign : '" + key + "' is not an option");
		return *this;
	}

	helper& fassign(const std::string& key, B fn){
		if(vflags.count(key)) fassigns.push_back(fassign_t({key, fn}));
		else throw lib::error::exception("assign : '" + key + "' is not a flag");
		return *this;
	}

	// PARSE

	template<typename P, typename O, typename F>
	helper& parse(int argc, char* argv[], P& params, O& options, F& flags){
		lib::pinput::parse(argc, argv, params,  options,  flags, this->options, this->flags);

		// RESOLVE ALIASES

		for(const auto& k : oaliases){
			if(options.count(k.second)){
				if(!options.count(k.first))
					options.insert(typename O::value_type(k.first, {}));

				options.at(k.first).insert(
					options.at(k.first).end(),
					options.at(k.second).begin(),
					options.at(k.second).end()
				);

				options.erase(k.second);
			}
		}


		for(const auto& k : faliases){
			if(flags.count(k.second)){
				if(!flags.count(k.first)) flags.insert(k.first);
				flags.erase(k.second);
			}
		}


		// RESOLVE DEFAULTS

		for(const auto& k : odefaults){
			if(!options.count(k.first)){
				options.insert(typename O::value_type(k.first, {k.second}));
			}
			else if(!options.at(k.first).size()){
				options.at(k.first) = k.second;
			}
		}

		// ASSIGN

		for(const auto& k : oassigns){
			if(options.count(k.key) && options.at(k.key).size()){
				try{
					(*k.fn)(options.at(k.key));
				}
				catch(const std::exception& e){
					throw lib::error::exception("parse : failed to parse '" + k.key +"' (" + e.what() + ")." );
				}
			}
		}


		for(const auto& k : fassigns){
			(*k.fn)(flags.count(k.key));
		}

		return *this;
	}

	// CHECK

	template<typename P, typename O, typename F>
	helper& validate(P&, O& options, F&){

		// CHECK MANDATORY

		for(const auto& d : omandatory){
			bool ok = false;
			for(const auto& c : d){
				bool conjunction_satisfied = true;
				for(const auto& v : c){
					if(!options.count(v) || !options.at(v).size()){
						conjunction_satisfied = false;
						break;
					}
				}
				if(conjunction_satisfied){
					ok = true;
					break;
				}
			}

			if(!ok){
				std::stringstream tmp;
				if(d.size() == 1){
					if(d[0].size() == 1){
						tmp << d[0][0] << " missing";
					}
					else{
						tmp << d[0] << " not satisfied";
					}
				}
				else{
					tmp << d << " not satisfied";
				}
				throw lib::error::exception(tmp.str());
			}
		}

		// CHECK CONDITIONS

		for(const auto& k : oconditions){
			if(!(*k.pred)())
				throw lib::error::exception("'" + k.key + "' condition " + k.msg);
		}

		return *this;
	}


	// USAGE

	std::string usage_msg;

	helper& usage(const std::string& msg){
		usage_msg = msg;
		return *this;
	}



};


	
} // pinput
} // lib

#endif // _LIB_PINPUT_HPP
