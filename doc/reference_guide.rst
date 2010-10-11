##############################
Reference Guide
##############################


.. _dynamic-messages:

******************
Dynamic logging
******************

Any functions in message args/fields are called and the value substitued:

>>> import os
>>> from twiggy.lib import thread_name
>>> thread_name()
'MainThread'
>>> log.fields(pid=os.getpid).info("I'm in thread {0}", thread_name) #doctest:+ELLIPSIS
INFO:pid=...:I'm in thread MainThread

This can be useful with partially-bound loggers, which let's us do some cool stuff:

>>> class ThreadTracker(object):
...     """a proxy that logs attribute access"""
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
Features are optional additons of logging functionality to the magic :data:`log`. They encapsulate common logging patterns. Code can be written using a feature, enhancing what information is logged. The feature can be disabled at :ref:`runtime <twiggy-setup>` if desired.

.. doctest::

    >>> import twiggy.features.socket
    >>> twiggy.quickSetup()
    >>> twiggy.log.addFeature(twiggy.features.socket.socket)
    >>> import socket
    >>> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #doctest:+ELLIPSIS
    <socket._socketobject object at 0x...>
    >>> s.connect(('www.python.org', 80))
    >>> twiggy.log.socket(s).debug("connected")
    DEBUG:host=dinsdale.python.org:ip_addr=82.94.164.162:port=80:service=http:connected
    >>> twiggy.log.disableFeature('socket')
    >>> twiggy.log.socket(s).debug("connected")
    DEBUG:connected
    >>> twiggy.log.addFeature(twiggy.features.socket.socket_minimal, 'socket')
    >>> twiggy.log.socket(s).debug("connected")
    DEBUG:ip_addr=82.94.164.162:port=80:connected


.. _wsgi-support:

WSGI Extension
==============
OMG it don't exist yet.

.. _never-raises:

***********************
Stays Out of Your Way
***********************
Twiggy tries to stay out of your way.  Specifically, an error in logging should **never** propogate outside the logging subsystem and cause your main application to crash. Instead, errors are trapped and reported by the  :data:`~twiggy.internal_log`.

Instances of :class:`~twiggy.logger.InternalLog` only have a single :class:`~twiggy.outputs.Output` - they do not use emitters. By default, these messages are sent to standard error. You may assign an alternate ouput (such as a file) to ``twiggy.internal_log.output` if desired, with the following conditions:

* the output should be failsafe - any errors that occur during internal logging will *not* be caught and will cause your application to crash.
* accordingly, networked or asynchronous outputs are not recommended.
* make sure someone is reading these log messages!

****************
Concurrency
****************
Locking in twiggy is as fine-grained as possible. Each individual output has its own lock (if necessary), and only holds that lock when writing. Using redundant outputs (ie, pointing to the same file) is not supported and will cause logfile corruption.

Asynchronous loggers never lock.

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
