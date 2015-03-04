
all:

	python3 run/compile.py build_ext --inplace

test:

	find src -name "*.py" -type f | xargs python3 -m doctest

testv:

	find src -name "*.py" -type f | xargs python3 -m doctest -v

clean:

	rm -f *.c
	rm -f *.so
	rm -rf build/
	rm -rf __pycache__/

boot:

	pip3 install numpy
	pip3 install cython
