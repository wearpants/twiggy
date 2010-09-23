###############
Basic Use
###############
This part describes how user code can log messages with twiggy.

:func:`pants`

***************
Setup is simple
***************
In your main.py:

>>> import twiggy
>>> twiggy.quick_setup()

.. seealso:: Full :doc:`configuration` details.

****************
Logging Messages
****************
The main interface is the the magic :class:`log <twiggy.Logger.Logger>`.

>>> from twiggy import log
>>> log #doctest:+ELLIPSIS
<twiggy.Logger.Logger object at 0x...>

It works out of the box, using typical :mod:`levels <Levels>`. Arbitrary levels are *not* supported.

>>> log.debug('You may not care')
DEBUG:You may not care
>>> log.error('OMFG! Pants on fire!')
ERROR:OMFG! Pants on fire!

The log can handle messages in several styles of :ref:`format strings<alternate-styles>`, defaulting to new-style.

>>> log.info('I wear {0} on my {where}', 'pants', where='legs')
INFO:I wear pants on my legs

You can name your loggers.

>>> mylog = log.name('alfredo')
>>> mylog.debug('hello')
DEBUG:alfredo:hello

**************
Better output
**************
Twiggy's default output strives to be user-friendly and to avoid pet peeves.

Newlines are suppressed by default; that can be turned off per-message.

>>> log.info('user\ninput\nannoys\nus')
INFO:user\ninput\nannoys\nus
>>> log.options(suppress_newlines=False).info('we\ndeal')
INFO:we
deal

Exceptions are prefixed by ``TRACE``. By default, :meth:`tracing <.Logger.trace>` will use the current exception, but you can also pass an exc_info tuple.

>>> try:
...     1/0
... except:
...     log.trace('error').warning('oh noes') #doctest:+ELLIPSIS
WARNING:oh noes
TRACE Traceback (most recent call last):
TRACE   File "<doctest notes.txt[...]>", line 2, in <module>
TRACE     1/0
TRACE ZeroDivisionError: integer division or modulo by zero

.. seealso:: :ref:`How to fold exceptions to a single line<folding-exceptions>`

******************
Method Chaining
******************
I like this chained style a lot.

>>> log.name('benito').info('hi there')
INFO:benito:hi there

It makes :term:`structured logging` easy. Rather than stuffing fielded data in the text of your message, use :meth:`~Logger.fields` to add arbitrary key-value pairs.  Output is easily parseable.

>>> log.fields(paths=42).info('Going for a walk')
INFO:paths=42:Going for a walk

The :meth:`struct` is a short cut for only logging fields. This is great for runtime statistics gathering.

>>> log.struct(paths=42, dolphins='thankful')
INFO:dolphins=thankful:paths=42:

Each call to ``fields`` or ``options`` creates a new, independent log instance that inherits all of the data of the parent.  This incremental binding can be useful for :ref:`webapps<wsgi-support>`.

>>> webapp_log = log.name("myblog")
>>> current_request_log = webapp_log.fields(request_id='12345')
>>> current_request_log.fields(rows=100, user='frank').info('frobnicating database')
INFO:myblog:request_id=12345:rows=100:user=frank:frobnicating database
>>> current_request_log.fields(bytes=5678).info('sending page over tubes')
INFO:myblog:bytes=5678:request_id=12345:sending page over tubes
>>> another_log = webapp_log.fields(request_id='67890')
>>> another_log.debug('Client connected')
DEBUG:myblog:request_id=67890:Client connected

Chained style is awesome. It allows you to create complex yet parsable log messages in a concise way.

>>> log.name('donjuan').fields(pants='sexy').info("hello, {who} want to {what}?", who='ladies', what='dance')
INFO:donjuan:pants=sexy:hello, ladies want to dance?

*************************
Sample Log
*************************
Routed to a `file <.FileOutputter>`, the above produces the following::

    2010-03-28T14:23:34:DEBUG:You may not care
    2010-03-28T14:23:34:ERROR:OMFG! Pants on fire!
    2010-03-28T14:23:34:INFO:I like bikes
    2010-03-28T14:23:34:INFO:I wear pants on my legs
    2010-03-28T14:23:34:DEBUG:alfredo:hello
    2010-03-28T14:23:34:INFO:user\ninput\nannoys\nus
    2010-03-28T14:23:34:INFO:we
    deal
    2010-03-28T14:23:34:WARNING:oh noes
    TRACE Traceback (most recent call last):
    TRACE   File "futz.py", line 35, in <module>
    TRACE     1/0
    TRACE ZeroDivisionError: integer division or modulo by zero
    2010-03-28T14:23:34:INFO:benito:hi there
    2010-03-28T14:23:34:INFO:paths=42:Going for a walk
    2010-03-28T14:23:34:INFO:dolphins=thankful:paths=42:
    2010-03-28T14:23:34:INFO:myblog:request_id=12345:rows=100:user=frank:frobnicating database
    2010-03-28T14:23:34:INFO:myblog:bytes=5678:request_id=12345:sending page over tubes
    2010-03-28T14:23:34:INFO:myblog:request_id=67890:Client connected
    2010-03-28T14:23:34:INFO:donjuan:pants=sexy:hello, ladies want to dance?
