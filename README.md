## GHC 2015 qualification round

# getting started

Make sure you have glpk (lib + header) files installed.
For example, on Ubuntu

	sudo apt-get install libglpk36 libglpk-dev

Running

	sudo make boot

will install Numpy, Cython and ecyglpki.

# guidelines

  - write readable Python 3
  - test each method with a few doctest

# run it

	./solve in/dc.in -f 3000 -l 200000 -s 2

# validate it

	./validate in/dc.in out/*

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
