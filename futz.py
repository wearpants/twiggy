import twiggy

twiggy.basicConfig()

# works out of the box; standard levels
twiggy.log.debug('You may not care')
twiggy.log.error('OMFG! Pants on fire!')

# support for format strings
twiggy.log.info('I like %s', "bikes")

# new style too
twiggy.log.info('I wear {0} on my {where}', 'pants', where='legs')

# named loggers
mylog = twiggy.log.name('alfredo')
mylog.debug('hello')

# this is not getLogger tho
twiggy.log.name('alfredo') is not mylog

# You don't need to store loggers
# I like this chained style a lot.
twiggy.log.name('benito').info('hi there')

# structured logging is easy
twiggy.log.fields(paths=42).info('Going for a walk')

# short cut.  great for runtime statistics gathering
twiggy.log.struct(paths=42, dolphins='thankful')

# This kind of partial binding is great for webapps
per_request_log = twiggy.log.fields(request_id='12345')
per_request_log.info('frobnicating database')
per_request_log.info('sending page over tubes')

# Chained style is awesome
twiggy.log.name('donjuan').fields(pants='sexy').info('hello, ladies')

# Exceptions.  Can also pass exc_info. Each line is prefixed.
try:
    1/0
except:
    twiggy.log.trace('error').warning('oh noes') # error is the default & can be omitted

# Newlines are suppressed by default; that can be turned off per-message
twiggy.log.info('user\ninput\nannoys\nus')
twiggy.log.options(suppress_newlines=False).info('we\ndeal')

# More fun. Any functions in args/fields are called and the value substitued.
import os
import threading

# we'll provide a useful collection of such things
def thread_name():
    return threading.currentThread().getName()

twiggy.log.fields(pid=os.getpid).info("I'm in thread {0}", thread_name)