#################
Logging Messages
#################

.. currentmodule:: twiggy

This part describes how user code can log messages with twiggy.

To get started quickly, use :func:`quick_setup`.::

    >>> import twiggy
    >>> twiggy.quick_setup()

.. seealso:: Full details on :doc:`configuration`.

****************
The Magic log
****************

The main interface is the the magic :data:`log`.

.. doctest:: magic-log

    >>> from twiggy import log
    >>> log
    <twiggy.logger.Logger object at 0x...>

It works out of the box, using typical :mod:`.levels`. Arbitrary levels are *not* supported. Note that when logging, you never need to refer to any level object; just use the methods on the log.

.. doctest:: magic-log

    >>> log.debug('You may not care')
    DEBUG|You may not care
    >>> log.error('OMFG! Pants on fire!')
    ERROR|OMFG! Pants on fire!

The log can handle messages in several styles of :ref:`format strings<alternate-styles>`, defaulting to `new-style <http://docs.python.org/library/string.html#format-string-syntax>`_.

.. doctest:: magic-log

    >>> log.info('I wear {0} on my {where}', 'pants', where='legs')
    INFO:I wear pants on my legs

You can name your loggers.

.. doctest:: magic-log

    >>> mylog = log.name('alfredo')
    >>> mylog.debug('hello')
    DEBUG:alfredo|hello

.. _better-output:

**************
Better output
**************
Twiggy's default output strives to be user-friendly and to avoid pet peeves.

Newlines are suppressed by default; that can be turned off per-message.

.. doctest:: better-output

    >>> log.info('user\ninput\nannoys\nus')
    INFO|user\ninput\nannoys\nus
    >>> log.options(suppress_newlines=False).info('we\ndeal')
    INFO|we
    deal

Exceptions are prefixed by ``TRACE``. By default, :meth:`tracing <.trace>` will use the current exception, but you can also pass an exc_info tuple.

.. doctest:: better-output

    >>> try:
    ...     1/0
    ... except:
    ...     log.trace('error').warning('oh noes')
    WARNING|oh noes
    TRACE Traceback (most recent call last):
    TRACE   File "<doctest better-output[...]>", line 2, in <module>
    TRACE ZeroDivisionError: integer division or modulo by zero

.. seealso:: :ref:`How to fold exceptions to a single line<folding-exceptions>`

.. _structured-logging:

**********************
Structured Logging
**********************
I like this method chaining style a lot.

.. doctest:: structured-logging

    >>> log.name('benito').info('hi there')
    INFO:benito|hi there

It makes :term:`structured logging` easy. In the past, fielded data was stuffed in the text of your message:

.. doctest:: structured-logging

    >>> log.info('Going for a walk. path: {0} roads: {1}', "less traveled", 42)
    INFO:Going for a walk. path: less traveled roads: 42

Instead, you can use :meth:`.fields` to add arbitrary key-value pairs.  Output is easily parseable.

.. doctest:: structured-logging

    >>> log.fields(path="less traveled", roads=42).info('Going for a walk')
    INFO:path=less traveled:roads=42|Going for a walk

The :meth:`.struct` is a short cut for *only* logging fields. This is great for runtime statistics gathering.

.. doctest:: structured-logging

    >>> log.struct(paths=42, dolphins='thankful')
    INFO:dolphins=thankful:paths=42|

****************************
Partial Binding
****************************

Each call to :meth:`.fields` or :meth:`.options` creates a new, independent log instance that inherits all of the data of the parent.  This incremental binding can be useful for webapps.

.. doctest:: partial-binding

    >>> ## an application-level log
    ... webapp_log = log.name("myblog")
    >>> ## a log for the individual request
    ... current_request_log = webapp_log.fields(request_id='12345')
    >>> current_request_log.fields(rows=100, user='frank').info('frobnicating database')
    INFO:myblog:request_id=12345:rows=100:user=frank|frobnicating database
    >>> current_request_log.fields(bytes=5678).info('sending page over tubes')
    INFO:myblog:bytes=5678:request_id=12345|sending page over tubes
    >>> ## a log for a different request
    ... another_log = webapp_log.fields(request_id='67890')
    >>> another_log.debug('Client connected')
    DEBUG:myblog:request_id=67890|Client connected

Chained style is awesome. It allows you to create complex yet parsable log messages in a concise way.

.. doctest:: partial-binding

    >>> log.name('donjuan').fields(pants='sexy').info("hello, {who} want to {what}?", who='ladies', what='dance')
    INFO:donjuan:pants=sexy|hello, ladies want to dance?

*************************
Sample Output
*************************

.. _sample-file-output:

Routed to a `file <.FileOutput>`, the above produces the following::

    2010-03-28T14:23:34Z:DEBUG:You may not care
    2010-03-28T14:23:34Z:ERROR:OMFG! Pants on fire!
    2010-03-28T14:23:34Z:INFO:I like bikes
    2010-03-28T14:23:34Z:INFO:I wear pants on my legs
    2010-03-28T14:23:34Z:DEBUG:alfredo:hello
    2010-03-28T14:23:34Z:INFO:user\ninput\nannoys\nus
    2010-03-28T14:23:34Z:INFO:we
    deal
    2010-03-28T14:23:34Z:WARNING:oh noes
    TRACE Traceback (most recent call last):
    TRACE   File "<doctest better-output[...]>", line 35, in <module>
    TRACE ZeroDivisionError: integer division or modulo by zero
    2010-03-28T14:23:34Z:INFO:benito:hi there
    2010-03-28T14:23:34Z:INFO:Going for a walk. path: less traveled roads: 42
    2010-03-28T14:23:34Z:INFO:path=less traveled:roads=42:Going for a walk
    2010-03-28T14:23:34Z:INFO:dolphins=thankful:paths=42:
    2010-03-28T14:23:34Z:INFO:myblog:request_id=12345:rows=100:user=frank:frobnicating database
    2010-03-28T14:23:34Z:INFO:myblog:bytes=5678:request_id=12345:sending page over tubes
    2010-03-28T14:23:34Z:INFO:myblog:request_id=67890:Client connected
    2010-03-28T14:23:34Z:INFO:donjuan:pants=sexy:hello, ladies want to dance?
    2010-03-28T14:23:34Z:INFO:myblog:request_id=12345:rows=100:user=frank:frobnicating database
    2010-03-28T14:23:34Z:INFO:myblog:bytes=5678:request_id=12345:sending page over tubes
    2010-03-28T14:23:34Z:DEBUG:myblog:request_id=67890:Client connected

