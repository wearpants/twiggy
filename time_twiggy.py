import twiggy.Emitter

import tempfile
import os

fname = tempfile.mktemp()
logfile = open(fname, 'w')

def output(msg, s):
    logfile.write(s)

my_emitter = twiggy.Emitter.Emitter(twiggy.Levels.DEBUG, True,
                                    twiggy.Emitter.LineFormatter().format,
                                    logfile.write)

twiggy.emitters['*'] = my_emitter

import timeit

loops = 100000

t = min(timeit.repeat( number = loops,
stmt="""log.debug('hello, ladies')""",
setup="""
import twiggy
log=twiggy.log.name('donjuan')
"""))
os.remove(fname)

print "{0:.3f} sec for {1:n} loops".format(t, loops)