#!/usr/bin/env python3
from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'firetiger',
  ext_modules = cythonize('*.pyx'),
)

