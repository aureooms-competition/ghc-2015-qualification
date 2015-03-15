#ifndef _LIB_RANDOM_SAMPLE_HPP
#define _LIB_RANDOM_SAMPLE_HPP

#include <stddef.h>
#include <algorithm>

namespace lib{
namespace random{

/**
 * Function template for array random sampling.
 * After call, sampling result is the n first elements of the array.
 * 
 * @author Ooms Aurélien
 *
 * @param <G> generator type
 * @param <D> distribution type
 * @param <A> array type
 * @param <T> indices type
 * 
 * @param generator
 * @param n number of elements to sample
 * @param a the array to sample
 * @param i begin
 * @param j end
 *
 */

template<typename G, typename D, typename A, typename T = size_t>
void sample(G& generator, const T n, A& a, const T i, const T j){


	T t = i - 1;
	const T x = i + n;
	
	while(++t < x){
		D randint(t, j - 1);
		const T k = randint(generator);
		std::swap(a[t], a[k]);
	}

}

} // random
} // lib

#endif // _LIB_RANDOM_SAMPLE_HPP