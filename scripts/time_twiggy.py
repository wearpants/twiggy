#! /usr/bin/env python
import twiggy

import tempfile
import os

fname = tempfile.mktemp()

twiggy.quickSetup(twiggy.levels.DEBUG, fname)
import timeit

loops = 100000

t = min(timeit.repeat( number = loops,
stmt="""log.debug('hello, ladies')""",
setup="""
import twiggy
log=twiggy.log.name('donjuan')
"""))
os.remove(fname)

print("{0:.3f} sec for {1:n} loops".format(t, loops))
