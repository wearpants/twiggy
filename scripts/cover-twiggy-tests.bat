rem find the unittest module
echo off
coverage erase
set COVERAGE_PROCESS_START=.coveragerc
set TWIGGY_UNDER_TEST=1
coverage run scripts/unittest_main.py %*
coverage combine
coverage html