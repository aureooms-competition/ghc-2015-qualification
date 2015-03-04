## GHC 2015 qualification round

# getting started

	sudo make boot

will install numpy and cython

# guidelines

  - write readable Python 3
  - test each method with a few doctest

# test it

no output if no error

	make test

or verbose

	make testv

# cythonize it

	make

Note that once cythonized `make test` and `make testv` will run tests for both
the source python code (.py) **and** the compiled share object (.so).
