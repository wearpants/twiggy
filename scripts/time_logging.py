#!/usr/bin/env python
import logging
import tempfile
import os

fname = tempfile.mktemp()

logging.basicConfig(level=logging.DEBUG,
                    filename = fname,
                    format='%(asctime)s %(levelname)s %(message)s',)



import timeit

loops = 100000

t = min(timeit.repeat( number = loops,
stmt="""log.debug('hello, ladies')""",
setup="""
import logging
log=logging.getLogger('donjuan')
"""))
os.remove(fname)

print "{0:.3f} sec for {1:n} loops".format(t, loops)
