#!/bin/bash
coverage erase
coverage run -a --branch --include="twiggy/*" `which unit2` discover
coverage run -a --branch --include="twiggy/*" `which sphinx-build` -b doctest -d doc/_build/doctrees doc doc/_build/doctest
coverage report -m

