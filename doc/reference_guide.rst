##############################
Reference Guide
##############################

.. currentmodule:: twiggy

.. _dynamic-messages:

******************
Dynamic Logging
******************

Any functions in message args/fields are called and the value substitued.

.. doctest:: dynamic-logging

    >>> import os
    >>> from twiggy.lib import thread_name
    >>> thread_name()
    'MainThread'
    >>> log.fields(pid=os.getpid).info("I'm in thread {0}", thread_name)
    INFO:pid=...:I'm in thread MainThread

This can be useful with partially-bound loggers, which lets us do some cool stuff. Here's a proxy class that logs which thread accesses attributes.

.. testcode:: dynamic-logging

    class ThreadTracker(object):
        """a proxy that logs attribute access"""
        def __init__(self, obj):
            self.__obj = obj
            # a partially bound logger
            self.__log = log.name("tracker").fields(obj_id=id(obj), thread=thread_name)
            self.__log.debug("started tracking")
        def __getattr__(self, attr):
            self.__log.debug("accessed {0}", attr)
            return getattr(self.__obj, attr)
    
    class Bunch(object):
        pass

Let's see it in action.

.. doctest:: dynamic-logging
    
    >>> foo = Bunch()
    >>> foo.bar = 42
    >>> tracked = ThreadTracker(foo)
    DEBUG:tracker:obj_id=...:thread=MainThread:started tracking
    >>> tracked.bar
    DEBUG:tracker:obj_id=...:thread=MainThread:accessed bar
    42
    >>> import threading
    >>> t=threading.Thread(target = lambda: tracked.bar * 2, name = "TheDoubler")
    >>> t.start(); t.join()
    DEBUG:tracker:obj_id=...:thread=TheDoubler:accessed bar

If you really want to log a callable, ``repr()`` it or wrap it in lambda.

.. seealso:: :mod:`.procinfo` feature

*******************
Features!
*******************
:mod:`Features <.features>` are optional additons of logging functionality to the `.log`. They encapsulate common logging patterns. Code can be written using a feature, enhancing what information is logged. The feature can be disabled at :ref:`runtime <twiggy-setup>` if desired.

.. warning:: Features are currently deprecated, pending a reimplementation in version 0.5

.. doctest:: features

    >>> from twiggy.features import socket as socket_feature
    >>> log.addFeature(socket_feature.socket)
    >>> import socket
    >>> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    >>> s.connect(('www.python.org', 80))
    >>> log.socket(s).debug("connected")
    DEBUG:host=dinsdale.python.org:ip_addr=82.94.164.162:port=80:service=www:connected
    >>> # turn off the feature - the name is still available
    ... log.disableFeature('socket')
    >>> log.socket(s).debug("connected")
    DEBUG:connected
    >>> # use a different implementation
    ... log.addFeature(socket_feature.socket_minimal, 'socket')
    >>> log.socket(s).debug("connected")
    DEBUG:ip_addr=82.94.164.162:port=80:connected

.. _never-raises:

***********************
Stays Out of Your Way
***********************
Twiggy tries to stay out of your way.  Specifically, an error in logging should **never** propogate outside the logging subsystem and cause your main application to crash. Instead, errors are trapped and reported by the  :data:`~twiggy.internal_log`.

Instances of :class:`.InternalLogger` only have a single :class:`.Output` - they do not use emitters. By default, these messages are sent to standard error. You may assign an alternate ouput (such as a file) to `twiggy.internal_log.output` if desired, with the following conditions:

* the output should be failsafe - any errors that occur during internal logging will be dumped to standard error, and suppressed, causing the original message to be discarded.
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
Libraries require special care to be polite and usable by application code.  The library should have a single bound in its top-level package that's used by modules. Library logging should generally be silent by default. ::

    # in mylib/__init__.py
    log = twiggy.log.name('mylib')
    log.min_level = twiggy.levels.DISABLED

    # in mylib/some_module.py
    from . import log
    log.debug("hi there")

This allows application code to enable/disable all of library's logging as needed. ::

    # in twiggy_setup
    import mylib
    mylib.log.min_level = twiggy.levels.INFO

In addition to :attr:`~.BaseLogger.min_level`, loggers also have a :attr:`~.Logger.filter`. This filter operates *only on the format string*, and is intended to allow users to selectively disable individual messages in a poorly-written library. ::

    # in mylib:
    for i in xrange(1000000):
        log.warning("blah blah {0}", 42)

    # in twiggy_setup: turn off stupidness
    mylib.log.filter = lambda format_spec: format_spec != "blah blah {0}"

Note that using a filter this way is an optimization - in general, application code should use :data:`emitters` instead.

********************
Tips And Tricks
********************

.. _alternate-styles:

Alternate Styles
================
In addition to the default new-style (braces) format specs, twiggy also supports old-style (percent, aka printf) and templates (dollar).

.. doctest:: alternate-styles

    >>> log.options(style='percent').info('I like %s', "bikes")
    INFO:I like bikes
    >>> log.options(style='dollar').info('$what kill', what='Cars')
    INFO:Cars kill

Use Fields
==========
Use :meth:`.fields` to include key-value data in a message instead of embedding it the human-readable string. ::

    # do this:
    log.fields(key1='a', key2='b').info("stuff happenend")

    # not this:
    log.info("stuff happened. key1: {0} key2: {1}", 'a', 'b')


**********************
Technical Details
**********************

Independence of logger instances
================================
Each log instance created by partial binding is independent from each other. In particular, a logger's :meth:`.name` has no relation to the object; it's just for human use.

.. doctest:: independent-loggers

    >>> log.name('bob') is log.name('bob')
    False

Optimizations
========================
Twiggy has been written to be fast, minimizing the performance impact on the main execution path. In particular, messages that will cause no output are handled as quickly as possible.  Users are therefore encouraged to add lots of logging for development/debugging purposes and then turn them off in production.

The emit methods can be hidden behind an appropriate ``assert``. Python will eliminate the statement entirely when run with bytecode optimization (``python -O``).

.. testcode:: optimizations

    assert log.debug("This goes away with python -O") is None
    assert not log.debug("So does this")
    
.. testoutput:: optimizations
    :hide:
    
    DEBUG:This goes away with python -O
    DEBUG:So does this
    
.. note:: The author doesn't particularly care for code written like this, but likes making his users happy more.

*******************
Extending Twiggy
*******************
When developing extensions to twiggy, use the :data:`devel_log`. An :class:`.InternalLogger`, the devel_log is completely separate from the main :data:`log`.  By default, messages logged to the devel_log are discarded; assigning an appropriate :class:`.Output` to its :attr:`~twiggy.devel_log.output` attribute before using.

Writing Features
===================

.. warning:: Features are currently deprecated, pending a reimplementation in version 0.5

Features are used to encapsulate common logging patterns. They are implemented as methods added to the :class:`.Logger` class. They receive an instance as the first argument (ie, ``self``). :meth:`Enable the feature <.addFeature>` before using.

Features come in two flavors: those that add information to a message's fields or set options, and those that cause output.

Features which only add fields/set options should simply call the appropriate method on ``self`` and return the resultant object.::

    def dimensions(self, shape):
        return self.fields(height=shape.height, width=shape.width)

Features can also emit messages as usual.  Do not return from these methods.::

    def sayhi(self, lang):
        if lang == 'en':
            self.info("Hello world")
        elif lang == 'fr':
            self.info("Bonjour tout le monde")

.. _wsgi-support:

If the feature should add fields *and* emit in the same step (like :meth:`.struct`), use the :func:`.emit` decorators.  Here's a prototype feature that dumps information about a `WSGI environ <http://www.python.org/dev/peps/pep-0333/#environ-variables>`_.::

    from twiggy.logger import emit

    @emit.info
    def dump_wsgi(self, wsgi_environ):
        keys = ['SERVER_PROTOCOL', 'SERVER_PORT', 'SERVER_NAME', 'CONTENT_LENGTH', 'CONTENT_TYPE', 'QUERY_STRING', 'PATH_INFO', 'SCRIPT_NAME', 'REQUEST_METHOD']
        d = {}
        for k in keys:
            d[k] = wsgi_environ.get(k, '')

        for k, v in wsgi_environ.iteritems():
            if k.startswith('HTTP_'):
                k = k[5:].title().replace('_', '-')
                d[k] = v

        # if called on an unnamed logger, add a name
        if name not in self._fields:
            self = self.name('dumpwsgi')

        return self.fieldsDict(d)

Writing Outputs and Formats
==============================
Outputs do the work of writing a message to an external resource (file, socket, etc.).  User-defined outputs should inherit from :class:`.Output` or :class:`.AsyncOutput` if they wish to support :term:`asynchronous logging` (preferred).

An Output subclass's ``__init__`` should take a :ref:`format <format-function>` and any parameters needed to acquire resources (filename, hostname, etc.), but *not the resources themselves*. These are created in :meth:`._open`.  Implementations supporting asynchronous logging should also take a :class:`msg_buffer <.AsyncOutput>` argument.


Outputs should define the following:

.. automethod:: twiggy.outputs.Output._open
    :noindex:

.. automethod:: twiggy.outputs.Output._close
    :noindex:

.. automethod:: twiggy.outputs.Output._write
    :noindex:

If the output requires locking to be thread-safe, set the class attribute :attr:`~.use_locks` to True (the default). Turning off may give slightly higher throughput.

The :attr:`format <.Output._format>` callable is Output-specific; it should take a :class:`.Message` and return an appropriate object (string, database row, etc.) to be written. **Do not modify** the received message - it is shared by all outputs.

.. _conversion-table-example:

:class:`ConversionTables<.ConversionTable>` are particulary useful for formatting fields. They are commonly used with :class:`.LineFormat` to format messages for text-oriented output.

.. testcode::
    
    from twiggy.lib.converter import ConversionTable
    conversion = ConversionTable()
    
    fields = {'shape': 'square',
              'height': 10,
              'width': 5,
              'color': 'blue'}

    # hide shape field name
    # uppercase value
    # make mandatory
    conversion.add(key = 'shape',
                   convertValue = str.upper,
                   convertItem = '{1}'.format, # stringify 2nd item (value)
                   required = True)
   
    # format height value with two decimal places
    # show as "<key> is <value>"
    conversion.add('height', '{0:.2f}'.format, "{0} is {1}".format)
   
    # separate fields in final output by colons
    conversion.aggregate = ':'.join
    
    # unknown items are sorted by key
    
    # unknown values are stringified
    conversion.genericValue = str
    
    # show unknown items as "<key>=<value>"
    conversion.genericItem = "{0}={1}".format
    
    # convert!
    print conversion.convert(fields)

.. testoutput::

    SQUARE:height is 10.00:color=blue:width=5
