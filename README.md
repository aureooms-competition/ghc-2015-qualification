## GHC 2015 qualification round

# getting started

Running

	sudo make boot

will install Numpy and Cython.

# guidelines

  - write readable Python 3
  - test each method with a few doctest

# test it

The "no output if no error" version.

	make test

The "verbose" version.

	make testv

# cythonize it

	make

Note that once cythonized `make test` and `make testv` will run tests for both
the source python code (.py) **and** the compiled share object (.so).

# clean it

Removes all cythonization artifacts.

	make clean
