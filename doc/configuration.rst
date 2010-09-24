######################
Configuration
######################

This part discusses how to configure twiggy's output of messages.  You should do this once, near the start of your application's ``__main__``.

*******************
Quick Setup
*******************

.. autodata:: twiggy.emitters

*******************
Modern design
*******************
Twiggy's output side features modern, loosely coupled design.

By convention, your configuration lives in a file in your application called ``twiggy_setup.py``, in a function called ``setup()``.  See an example. XXX link here! We'll be running through similar commands in a shell to demonstrate.

The :data:`~twiggy.emitters` dictionary is the root of all evil. It's linked to the :data:`~twiggy.log`.

>>> from twiggy.setup import * # quick_setup, outputs, formats, filters, emitters, levels, addEmitters
>>> emitters
{}

You can quickly set up using quick_setup:

>>> setup = quick_setup()
>>> # in the top of your __main__:
>>> setup()

.. autofunction:: twiggy.quick_setup

Controlling what comes out
===========================
Filters and min_level can be changed during the runnning of an app; outputters & formatters cannot; instead, remove the emitter and create a new one.

You can set a min_level on Emitters.

>>> from twiggy import log
>>> emitters['*'].min_level = levels.INFO
>>> log.debug("Help, help I'm being suppressed")
>>> log.info("I'm not quite dead yet")
INFO:I'm not quite dead yet

You can filter on regexes, or with arbitrary functions:

>>> emitters['*'].filter = ".*pants.*"
>>> log.info("Got my {0} on", "pants")
INFO:Got my pants on
>>> log.info("Got my {0} on", "shirt")

Let's reset all that:

>>> twiggy.emitters['*'].filter = True
>>> twiggy.emitters['*'].min_level = twiggy.Levels.DEBUG

Create some outputs

>>> import sys, copy, pprint
>>> shell_output = outputs.StreamOutputter(formats.shell_format, stream=sys.stderr)

.. seealso: :class:`FileOutputter`, more useful for a real config

You can add emitters easily, using the convenience :func:`addEmitters`

>>> addEmitters( # tuple of: emitter_name, min_level, filter, outputter
                ("everything", levels.DEBUG, True, shell_output),
                ("thieves", levels.INFO, filters.names("bonnie", "clyde"), shell_output))
>>> pprint.pprint(emitters) #doctest:+ELLIPSIS
{'everything': <twiggy.Emitter.Emitter object at 0x...>,
'thieves': <twiggy.Emitter.Emitter object at 0x...>}

.. autofunction:: twiggy.addEmitters

:data:`twiggy.emitters` is the root. Demo :func:`twiggy.addEmitters`.

Modern design (like django!)

**********************
Emitter Objects
**********************

Emitters
========
filter + outputter

Filters
=======
take mesg, return bool. names, glob_names

Outputters
==========
paired with a formatter, do work of writing

Formatter
==========
<mumble>

.. _folding-exceptions:

You can fold exceptions by usin '\\n' as a prefix to fold into a single line.

***********************
Real config
***********************
Your app should put it's configuration in a file called ``tiwggy_setup.py`` somewhere.  It looks like::

    from twiggy.setup import * # outputs, filters, formats, levels, addEmitters
    def setup():
    addEmitters(...)

And then somewhere near the top of your main, do::

    import twiggy_setup
    twiggy_setup.setup()    

You could import alternate modules (``twiggy_setup_prod.py``), or use alternate function names (``twiggy_setup.setup_devel()``) whatever your CMS-loving heart desires!

Async Output
============
how it goes

Example configs
===============
a few

Log-level config
================
Library should be silent by default - set :attr:`Logger.min_level` to `Levels.Disabled`
 


Logger.filter, used to turn off stupidness


