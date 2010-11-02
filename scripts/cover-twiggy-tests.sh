#!/bin/bash
coverage erase
COVERAGE_PROCESS_START=.coveragerc coverage run `which unit2` discover
coverage combine
coverage html

