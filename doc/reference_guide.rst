##############################
Reference Guide
##############################


.. _dynamic-messages:

******************
Dynamic!
******************

Any functions in args/fields are called and the value substitued:

>>> import os
>>> from twiggy.lib import thread_name
>>> thread_name()
'MainThread'
>>> log.fields(pid=os.getpid).info("I'm in thread {0}", thread_name) #doctest:+ELLIPSIS
INFO:pid=...:I'm in thread MainThread

This can be useful with partially-bound loggers, which let's us do some cool stuff:

>>> class ThreadTracker(object):
...     def __init__(self, obj):
...         self.__obj = obj
...         # a partially bound logger
...         self.__log = log.name("tracker").fields(obj_id=id(obj), thread=thread_name)
...         self.__log.debug("started tracking")
...     def __getattr__(self, attr):
...         self.__log.debug("accessed {0}", attr)
...         return getattr(self.__obj, attr)
...
>>> class Bunch(object):
...     pass
...
>>> foo = Bunch()
>>> foo.bar = 42
>>> tracked = ThreadTracker(foo) #doctest:+ELLIPSIS
DEBUG:tracker:obj_id=...:thread=MainThread:started tracking
>>> tracked.bar #doctest:+ELLIPSIS
DEBUG:tracker:obj_id=...:thread=MainThread:accessed bar
42
>>> import threading
>>> t=threading.Thread(target = lambda: tracked.bar * 2, name = "TheDoubler")
>>> t.start(); t.join() #doctest:+ELLIPSIS
DEBUG:tracker:obj_id=...:thread=TheDoubler:accessed bar

If you really want to log a callable, ``repr()`` it or wrap it in lambda.

*******************
Features!
*******************
Twiggy supports adding additional functionality to :data:`log` using features.

.. _wsgi-support:

WSGI Extension
==============
OMG it don't exist yet.

.. _never-raises:

***********************
Stays Out of Your Way
***********************
error handling, safety.  Logging should **never** interrrupt the flow of your main app (ie, cause erorrs).  Reported w/ internal_log

The internal log
================
:class:`twiggy.logger.InternalLog` just has an output, no emitters.  Using async is highly discouraged.

****************
Concurrency
****************
what's threadsafe, what's not

*******************
Use by Libraries
*******************
Library should be silent by default - set :attr:`Logger.min_level` to `levels.DISABLED`

Logger.filter, used to turn off stupidness

********************
Tips And Tricks
********************

.. _alternate-styles:

Alternate Styles
================
Old style works fine though:

>>> log.options(style='percent').info('I like %s', "bikes")
INFO:I like bikes

As do templates:

>>> log.options(style='dollar').info('$what kill', what='Cars')
INFO:Cars kill

Use Fields
==========
use fields instead of "Foo happend. key1:x1, key2:x2" in message

**********************
Technical Details
**********************

Independence of logger instances
================================
But the name has no relation to the object; it's just for human use:

>>> mylog is log.name('alfredo')
False

Internal optimizations
========================
it goes fast!

*******************
Extending Twiggy
*******************

the :data:`~twiggy.devel_log`

Writing Features
===================
How to do that

Writing Outputs
===================
How to do that

Writing Formats
===================
How to do that, including :class:`~twiggy.lib.ConversionTable`
