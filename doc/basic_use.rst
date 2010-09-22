###############
Basic Use
###############
This part describes how user code can log messages with twiggy.

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

>>> from twiggy import *

The main interface is the the magic **:class:`log <Logger>`**:

>>> log #doctest:+ELLIPSIS
<twiggy.Logger.Logger object at 0x...>

It works out of the box, using standard :module:`levels <Levels>` :

>>> log.debug('You may not care')
DEBUG:You may not care
>>> log.error('OMFG! Pants on fire!')
ERROR:OMFG! Pants on fire!

It supports a :ref:`variety of format strings<alternate-styles>`, defaulting to new-style:

>>> log.info('I wear {0} on my {where}', 'pants', where='legs')
INFO:I wear pants on my legs

You can name your loggers:

>>> mylog = log.name('alfredo')
>>> mylog.debug('hello')
DEBUG:alfredo:hello

**************
Better output
**************
Newlines are suppressed by default; that can be turned off per-message:

>>> log.info('user\ninput\nannoys\nus')
INFO:user\ninput\nannoys\nus

>>> log.options(suppress_newlines=False).info('we\ndeal')
INFO:we
deal

Exceptions are prefixed. Can also pass exc_info.

.. seealso:: :ref:`How to fold exceptions to a single line<folding-exceptions>`

>>> try:
...     1/0
... except:
...     log.trace('error').warning('oh noes') #doctest:+ELLIPSIS
WARNING:oh noes
TRACE Traceback (most recent call last):
TRACE   File "<doctest notes.txt[...]>", line 2, in <module>
TRACE     1/0
TRACE ZeroDivisionError: integer division or modulo by zero

******************
Method Chaining
******************
I like this chained style a lot.

>>> log.name('benito').info('hi there')
INFO:benito:hi there

It makes :term:`structured logging` easy:

>>> log.fields(paths=42).info('Going for a walk')
INFO:paths=42:Going for a walk

Short cut.  Great for runtime statistics gathering.

>>> log.struct(paths=42, dolphins='thankful')
INFO:dolphins=thankful:paths=42:

Partial binding can be useful for :ref:`webapps<wsgi-support>`:

>>> per_request_log = log.fields(request_id='12345')
>>> per_request_log.fields(rows=100, user='frank').info('frobnicating database')
INFO:request_id=12345:rows=100:user=frank:frobnicating database
>>> per_request_log.fields(bytes=5678).info('sending page over tubes')
INFO:bytes=5678:request_id=12345:sending page over tubes

Chained style is awesome:

>>> log.name('donjuan').fields(pants='sexy').info("hello, {who} want to {what}?", who='ladies', what='dance')
INFO:donjuan:pants=sexy:hello, ladies want to dance?

*************************
Sample Log
*************************
Routed to a file, the above produces the following::

    2010-03-28T00:23:34:DEBUG:You may not care
    2010-03-28T00:23:34:ERROR:OMFG! Pants on fire!
    2010-03-28T00:23:34:INFO:I like bikes
    2010-03-28T00:23:34:INFO:I wear pants on my legs
    2010-03-28T00:23:34:DEBUG:alfredo:hello
    2010-03-28T00:23:34:INFO:user\ninput\nannoys\nus
    2010-03-28T00:23:34:INFO:we
    deal
    2010-03-28T00:23:34:WARNING:oh noes
    TRACE Traceback (most recent call last):
    TRACE   File "futz.py", line 35, in <module>
    TRACE     1/0
    TRACE ZeroDivisionError: integer division or modulo by zero
    2010-03-28T00:23:34:INFO:benito:hi there
    2010-03-28T00:23:34:INFO:paths=42:Going for a walk
    2010-03-28T00:23:34:INFO:dolphins=thankful:paths=42:
    2010-03-28T00:23:34:INFO:request_id=12345:rows=100:user=frank:frobnicating database
    2010-03-28T00:23:34:INFO:bytes=5678:request_id=12345:sending page over tubes
    2010-03-28T00:23:34:INFO:donjuan:pants=sexy:hello, ladies want to dance?
