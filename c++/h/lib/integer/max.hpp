#ifndef _LIB_INTEGER_MAX_HPP
#define _LIB_INTEGER_MAX_HPP


namespace lib {
namespace integer {

/**
 * Function template for integer max selection without branching.
 *
 * @author Ooms Aurélien
 *
 * @param <T> integer type
 * 
 * @param a
 * @param b
 * 
 * @return a if a > b else b
 *
 */

template<typename T>
inline T max(const T& a, const T& b){
	const T i = -(a > b);
	return (a & i)|(b & ~i);
}


} // integer
} // lib


#endif // _LIB_INTEGER_MAX_HPP