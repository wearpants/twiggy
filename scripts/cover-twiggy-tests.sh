#!/bin/bash

# find the unittest module
coverage erase
COVERAGE_PROCESS_START=.coveragerc TWIGGY_UNDER_TEST=1 coverage run scripts/unittest_main.py $@
coverage combine
coverage html

