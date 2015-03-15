#ifndef _LIB_IO_HPP
#define _LIB_IO_HPP

#include <vector>
#include <map>
#include <queue>
#include <list>
#include <set>
#include <tuple>

namespace lib{
namespace io{

/**
 * Array of array-style punctuation.
 */
const char* list_p[] = {"[", "]", ", "};


/**
 * Array of set/map-style punctuation.
 */
const char* map_p[]  = {"{", "}", ", ", " : "};

/**
 * Array of tuple-style punctuation.
 */
const char* tuple_p[] = {"(", ")", ", "};


/**
 * Function template for std::vector formatting.
 * 
 * @author Ooms Aurélien
 * 
 * @param <S> the outstream type  
 * @param <T> the value type
 * 
 * @param out the outstream to write to
 * @param vector the vector to format
 * @param p the punctuation array
 * 
 * @return the outstream ref
 *
 */

template<typename S, typename T>
S& format(S& out, const std::vector<T>& vector, const char* p[] = list_p){
	out << p[0];
	if(!vector.empty()){
		for (size_t index = 0; index < vector.size()-1; ++index){
			out << vector[index];
			out << p[2];
		}
		out << vector[vector.size()-1];
	}
	out << p[1];
	return out;
}


/**
 * Function template for std::list formatting.
 * 
 * @author Ooms Aurélien
 * 
 * @param <S> the outstream type  
 * @param <T> the value type
 * 
 * @param out the outstream to write to
 * @param list the list to format
 * @param p the punctuation array
 * 
 * @return the outstream ref
 *
 */

template<typename S, typename T>
S& format(S& out, const std::list<T>& list, const char* p[] = list_p){
	out << p[0];
	if(!list.empty()){
		typename std::list<T>::const_iterator it = list.cbegin();
		out << *it;
		for (++it; it != list.cend(); ++it){
			out << p[2];
			out << *it;
		}
	}
	out << p[1];
	return out;
}


/**
 * Function template for std::queue formatting. /!\ The queue is copied.
 * 
 * @author Ooms Aurélien
 * 
 * @param <S> the outstream type  
 * @param <T> the value type
 * 
 * @param out the outstream to write to
 * @param queue the queue to format
 * @param p the punctuation array
 * 
 * @return the outstream ref
 *
 */

template<typename S, typename T>
S& format(S& out, std::queue<T> queue, const char* p[] = list_p){
	out << p[0];
	if(!queue.empty()){
		while(queue.size() > 1){
			out << queue.front();
			queue.pop();
			out << p[2];
		}
		out << queue.front();
		queue.pop();
	}
	out << p[1];
	return out;
}


/**
 * Function template for std::map formatting.
 * 
 * @author Ooms Aurélien
 * 
 * @param <S> the outstream type
 * @param <K> the key type
 * @param <T> the value type
 * 
 * @param out the outstream to write to
 * @param map the map to format
 * @param p the punctuation array
 * 
 * @return the outstream ref
 *
 */

template<typename S, typename K, typename T>
S& format(S& out, const std::map<K,T>& map, const char* p[] = map_p){
	out << p[0];
	if (map.size() > 0){
		typename std::map<K,T>::const_iterator it, pen = --map.end();
		for(it = map.begin(); it != pen; ++it){
			out << it->first;
			out << p[3];
			out << it->second;
			out << p[2];
		}
		out << it->first;
		out << p[3];
		out << it->second;
	}
	out << p[1];
	return out;
}


/**
 * Function template for std::multimap formatting.
 * 
 * @author Ooms Aurélien
 * 
 * @param <S> the outstream type
 * @param <K> the key type
 * @param <T> the value type
 * 
 * @param out the outstream to write to
 * @param multimap the multimap to format
 * @param p the punctuation array
 * 
 * @return the outstream ref
 *
 */

template<typename S, typename K, typename T>
S& format(S& out, const std::multimap<K,T>& map, const char* p[] = map_p){
	out << p[0];
	if (map.size() > 0){
		typename std::multimap<K,T>::const_iterator it, pen = --map.end();
		for(it = map.begin(); it != pen; ++it){
			out << it->first;
			out << p[3];
			out << it->second;
			out << p[2];
		}
		out << it->first;
		out << p[3];
		out << it->second;
	}
	out << p[1];
	return out;
}


/**
 * Function template for std::set formatting.
 * 
 * @author Ooms Aurélien
 * 
 * @param <S> the outstream type
 * @param <T> the value type
 * 
 * @param out the outstream to write to
 * @param set the set to format
 * @param p the punctuation array
 * 
 * @return the outstream ref
 *
 */

template<typename S, typename T>
S& format(S& out, const std::set<T>& set, const char* p[] = map_p){
	out << p[0];
	if(set.size() > 0){
		typename std::set<T>::const_iterator it = set.cbegin();
		out << *it;
		for (++it; it != set.cend(); ++it){
			out << p[2];
			out << *it;
		}
	}
	out << p[1];
	return out;
}

/**
 * Function template for std::tuple formatting.
 * 
 * @author Ooms Aurélien
 * 
 * @param <S> the outstream type
 * @param <T> the value type
 * 
 * @param out the outstream to write to
 * @param set the set to format
 * @param p the punctuation array
 * 
 * @return the outstream ref
 *
 */

template<size_t> struct int_{};

template <typename S, typename ... Args, size_t pos>
S& _format(S& out, const std::tuple<Args...>& t, const char* p[], int_<pos>) {
	out << std::get< std::tuple_size<std::tuple<Args...>>::value - pos>(t);
	out << p[2];
	return _format(out, t, p, int_<pos-1>());
}

template <typename S, typename ... Args>
S& _format(S& out, const std::tuple<Args...>& t, const char**, int_<1>) {
	out << std::get<std::tuple_size<std::tuple<Args...>>::value - 1>(t);
	return out;
}

template <typename S, typename ... Args>
S& format(S& out, const std::tuple<Args...>& t, const char* p[] = tuple_p) {
	out << p[0];
	_format(out, t, tuple_p, int_<sizeof...(Args)>());
	out << p[1];
	return out;
}

} // io
} // lib


/**
 * Alias of lib::io::format<S,T>(S&, std::vector<T>&)
 */

template<typename S, typename T>
S& operator<<(S& out, const std::vector<T>& vector){
	return lib::io::format(out, vector);
}


/**
 * Alias of lib::io::format<S,T>(S&, std::list<T>&)
 */

template<typename S, typename T>
S& operator<<(S& out, const std::list<T>& list){
	return lib::io::format(out, list);
}


/**
 * Alias of lib::io::format<S,T>(S&, std::queue<T>&)
 */

template<typename S, typename T>
S& operator<<(S& out, std::queue<T> queue){
	return lib::io::format(out, queue);
}


/**
 * Alias of lib::io::format<S,K,T>(S&, std::map<T>&)
 */

template<typename S, typename K, typename T>
S& operator<<(S& out, const std::map<K,T>& map){
	return lib::io::format(out, map);
}


/**
 * Alias of lib::io::format<S,K,T>(S&, std::multimap<T>&)
 */

template<typename S, typename K, typename T>
S& operator<<(S& out, const std::multimap<K,T>& map){
	return lib::io::format(out, map);
}


/**
 * Alias of lib::io::format<S,T>(S&, std::set<T>&)
 */

template<typename S, typename T>
S& operator<<(S& out, const std::set<T>& set){
	return lib::io::format(out, set);
}

/**
 * Alias of lib::io::format<S,... Args>(S&, std::tuple<Args...>&)
 */
 
template <typename S, typename ... Args>
S& operator<<(S& out, const std::tuple<Args...>& t) {
	return lib::io::format(out, t);
}


#endif //_LIB_IO_HPP
