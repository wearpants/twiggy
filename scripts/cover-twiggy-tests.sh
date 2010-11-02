#!/bin/bash

# find the unittest module
coverage erase
COVERAGE_PROCESS_START=.coveragerc coverage run scripts/unittest_stub.py discover
coverage combine
coverage html

