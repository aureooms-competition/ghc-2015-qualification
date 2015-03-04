from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
  name = 'Google Hash Code 2015 qualification round HDJKFHEU',
  ext_modules = cythonize( "src/*.py" , include_path = [numpy.get_include()]),
)

