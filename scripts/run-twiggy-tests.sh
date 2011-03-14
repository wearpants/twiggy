#!/bin/bash
TWIGGY_UNDER_TEST=1 python2.7 -m unittest discover -b
sphinx-build -b doctest -d doc/_build/doctrees doc doc/_build/doctest

