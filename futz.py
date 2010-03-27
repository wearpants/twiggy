#!/usr/bin/env python
## A file to futz around in ##

## Simple setup
import twiggy
twiggy.basicConfig()

## User-facing features
from twiggy import *

#the magic log
log

# works out of the box; standard levels
log.debug('You may not care')
log.error('OMFG! Pants on fire!')

# support for format strings
log.info('I like %s', "bikes")

# new style are preferred tho
log.info('I wear {0} on my {where}', 'pants', where='legs')

# named loggers
mylog = log.name('alfredo')
mylog.debug('hello')

## Better output
# Newlines are suppressed by default; that can be turned off per-message
log.info('user\ninput\nannoys\nus')
log.options(suppress_newlines=False).info('we\ndeal')

# Exceptions.  Can also pass exc_info. Each line is prefixed.
try:
    1/0
except:
    log.trace('error').warning('oh noes') # error is the default & can be omitted

## Method Chaining
# this is not getLogger tho
print log.name('alfredo') is not mylog

# You don't need to store loggers
# I like this chained style a lot.
log.name('benito').info('hi there')

# structured logging is easy
log.fields(paths=42).info('Going for a walk')

# short cut.  great for runtime statistics gathering
log.struct(paths=42, dolphins='thankful')

# This kind of partial binding is great for webapps
per_request_log = log.fields(request_id='12345')
per_request_log.info('frobnicating database')
per_request_log.info('sending page over tubes')

# Chained style is awesome
log.name('donjuan').fields(pants='sexy').info('hello, ladies')

## Dynamic
# More fun. Any functions in args/fields are called and the value substitued.
import os
import threading

# we'll provide a useful collection of such things
def thread_name():
    return threading.currentThread().getName()

log.fields(pid=os.getpid).info("I'm in thread {0}", thread_name)

## Optimizations
# loggers can take a min_level
mylog.min_level = twiggy.Levels.INFO
mylog.info("You see this")
mylog.debug("This is hidden")

# Also take a filter that operates on format_spec. Use case is efficiently
# shutting off specific messages in a library which is doing something stupid
mylog.filter = lambda s: "shenanigans" not in s
mylog.info("Starting silliness")
for i in xrange(3): # or much larger
    mylog.info("I call shenanigans!")
mylog.info("End silliness")