######################
Configuring Output
######################

This part discusses how to configure twiggy's output of messages.  You should do this once, near the start of your application's ``__main__``.

*******************
Quick Setup
*******************
To quickly configure output, use the `quickSetup` function.  Quick setup is limited to sending all messages to a file or ``sys.stderr``.  A timestamp will be prefixed when logging to a file.

.. autofunction:: twiggy.quickSetup

*******************
twiggy_setup.py
*******************
Twiggy's output side features modern, loosely coupled design.

By convention, your configuration lives in a file in your application called ``twiggy_setup.py``, in a function called ``twiggy_setup()``. You can of course put your configuration elsewhere, but using a separate module makes integration with configuration management systems easy.  You should import and run twiggy setup near the top of your application.  It's particularly important to set up twiggy *before spawning new processes*.

A ``twiggy_setup`` function should create ouputs and use the :func:`addEmitters` convenience function to link those outputs to the log:

.. testcode::

    from twiggy import *
    def twiggy_setup():
        alice_output = outputs.FileOutput("alice.log", format=formats.line_format)
        bob_output = outputs.FileOutput("bob.log", format=formats.line_format)

        addEmitters(
            # (name, min_level, filter, output),
            ("alice", levels.DEBUG, None, alice_output),
            ("betty", levels.INFO, filters.names("betty"), bob_output),
            ("brian.*", levels.DEBUG, filters.glob_names("brian.*"), bob_output),
            )

    # near the top of your __main__
    twiggy_setup()


In this example, we create two log destinations: ``alice.log`` and ``bob.log``.  alice will recieve all messages, and bob will receive two sets of messages:

* messages with the name field equal to ``betty`` and level >= ``INFO``
* messages with the name field glob-matching ``brian.*``

``addEmitters`` populates the `twiggy.emitters` dictionary:

.. doctest::

    >>> emitters.keys()
    ['alice', 'betty', 'brian.*']

:class:`Emitters <Emitter>` can be removed by deleting them from this dict. The filters and min_level may be modified during the running of the application, but outputs can *not* be changed.  Instead, remove the emitter and re-add it.

.. doctest::

    >>> # bump level
    ... emitters['alice'].min_level = levels.WARNING
    >>> # change filter
    ... emitters['alice'].filter = filters.names('alice', 'andy')
    >>> # remove entirely
    ... del emitters['alice']

We'll be examining the various parts in more detail.

**************************
Outputs
**************************
Outputs are the destinations to which log messages are written (files, databases, etc.). :mod:`Several implementations <outputs>` are provided. Once created, outputs cannot be modified.  Each output has an associated ``format``, described below.

.. _async-logging
Asynchronous Logging
====================
Many outputs can be configured to use a separate, dedicated process to log messages. This is known as :term:`asynchronous logging` and is enabled with the ``msg_buffer`` argument:

.. autoclass:: twiggy.outputs.AsyncOutput

Asynchronous mode dramatically reduces the cost of logging, as expensive formatting and writing operations are moved out of the main thread of control.

.. warning: There is a slight, but non-zero, chance that messages may be lost if something goes awry with the child process.


Controlling what comes out
===========================
Filters and min_level can be changed during the runnning of an app; outputs & formats cannot; instead, remove the emitter and create a new one.

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
>>> twiggy.emitters['*'].min_level = twiggy.levels.DEBUG

Create some outputs

>>> import sys, copy, pprint
>>> shell_output = outputs.StreamOutput(formats.shell_format, stream=sys.stderr)

.. seealso: :class:`FileOutput`, more useful for a real config

You can add emitters easily, using the convenience :func:`addEmitters`

>>> addEmitters( # tuple of: emitter_name, min_level, filter, output
                ("everything", levels.DEBUG, True, shell_output),
                ("thieves", levels.INFO, filters.names("bonnie", "clyde"), shell_output))
>>> pprint.pprint(emitters) #doctest:+ELLIPSIS
{'everything': <twiggy.filters.Emitter object at 0x...>,
'thieves': <twiggy.filters.Emitter object at 0x...>}

.. autofunction:: twiggy.addEmitters

:data:`twiggy.emitters` is the root. Demo :func:`twiggy.addEmitters`.

Modern design (like django!)

**********************
Emitter Objects
**********************

Emitters
========
filter + output

Filters
=======
take mesg, return bool. names, glob_names

Outputs
==========
paired with a format, do work of writing

format
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
Library should be silent by default - set :attr:`Logger.min_level` to `levels.DISABLED`



Logger.filter, used to turn off stupidness
