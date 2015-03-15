#ifndef _LIB_ERROR_EXCEPTION_HPP
#define _LIB_ERROR_EXCEPTION_HPP

#include <exception>
#include <string>

namespace lib{
namespace error{

/**
 * Base class for dynamic message exceptions.
 * 
 * @author Ooms Aurélien
 */

class exception : public std::exception {
private:
	std::string msg;
public:
	exception(const std::string& msg):msg(msg){}
	virtual ~exception() throw() {}
	const char* what() const throw() {return msg.c_str();}
};

} // error
} // lib


#endif // _LIB_ERROR_EXCEPTION_HPP