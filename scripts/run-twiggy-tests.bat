echo off

set TWIGGY_UNDER_TEST=1
python -m unittest discover -b

rem Need to 'unset' this envvar for the doctests to work
set TWIGGY_UNDER_TEST=
sphinx-build -b doctest -d doc\_build\doctrees doc doc\_build\doctest