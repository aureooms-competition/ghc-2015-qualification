#ifndef _LIB_ARRAY_PROXY_HPP
#define _LIB_ARRAY_PROXY_HPP

#include <stddef.h>

namespace lib{
namespace array{

/**
 * Class template for bidimensional array subscripting using a proxy.
 * 
 * <p>
 * Class template for bidimensional array subscripting using a proxy.
 * Note that no range checking is done.
 * 
 * @author Ooms Aurélien
 * 
 * @param <T> array value type
 *
 */
	
template<typename T>
class proxy{

private:

	T* pt;
	T** addr;
	size_t h, w;

	void alloc(){
		addr = new T*[h];
		for(size_t i = 0; i < h; ++i) addr[i] = pt + i * w;
	}

public:

	proxy() : addr(NULL){}

	proxy(T* pt, const size_t h, const size_t w) : pt(pt), addr(NULL), h(h), w(w){
		alloc();
	}

	void resize(T* pt, const size_t h, const size_t w){
		this->pt = pt;
		this->h = h;
		this->w = w;
		delete[] addr;
		alloc();
	}

	inline T* operator[](const size_t i){
		return addr[i];
	}

	inline const T* operator[](const size_t i) const{
		return addr[i];
	}

	~proxy(){
		delete[] addr;
	}



};



} // array
} // lib



#endif // _LIB_ARRAY_PROXY_HPP