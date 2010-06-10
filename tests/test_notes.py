import unittest2
import doctest

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocFileSuite("../notes.txt", module_relative=True))
    return tests
