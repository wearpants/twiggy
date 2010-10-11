######################
Configuring Output
######################

This part discusses how to configure twiggy's output of messages.  You should do this once, near the start of your application's ``__main__``.

*******************
Quick Setup
*******************
To quickly configure output, use the `quickSetup` function.  Quick setup is limited to sending all messages to a file or ``sys.stderr``.  A timestamp will be prefixed when logging to a file.

.. autofunction:: twiggy.quickSetup
    :noindex:

.. _twiggy-setup:

*******************
twiggy_setup.py
*******************
Twiggy's output side features modern, loosely coupled design.

By convention, your configuration lives in a file in your application called ``twiggy_setup.py``, in a function called ``twiggy_setup()``. You can of course put your configuration elsewhere, but using a separate module makes integration with configuration management systems easy.  You should import and run ``twiggy_setup`` near the top of your application.  It's particularly important to set up twiggy *before spawning new processes*.

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

:class:`Emitters <Emitter>` can be removed by deleting them from this dict. The filters and min_level may be modified during the running of the application, but outputs *cannot* be changed.  Instead, remove the emitter and re-add it.

.. doctest::

    >>> # bump level
    ... emitters['alice'].min_level = levels.WARNING
    >>> # change filter
    ... emitters['alice'].filter = filters.names('alice', 'andy')
    >>> # remove entirely
    ... del emitters['alice']

We'll examine the various parts in more detail.

**************************
Outputs
**************************
Outputs are the destinations to which log messages are written (files, databases, etc.). :mod:`Several implementations <outputs>` are provided. Once created, outputs cannot be modified.  Each output has an associated ``format``.

.. _async-logging:

Asynchronous Logging
====================
Many outputs can be configured to use a separate, dedicated process to log messages. This is known as :term:`asynchronous logging` and is enabled with the ``msg_buffer`` argument:

.. autoclass:: twiggy.outputs.AsyncOutput
    :noindex:

Asynchronous mode dramatically reduces the cost of logging, as expensive formatting and writing operations are moved out of the main thread of control.

.. warning: There is a slight, but non-zero, chance that messages may be lost if something goes awry with the child process.

*********************
Formats
*********************
:mod:`Formats <twiggy.formats>` transform a log message into a form that can be written by an output. The result of formatting is output-dependent - for example, an output that posts to an HTTP server may take a format that provides JSON, whereas an output that writes to a file may produce text.

Line-oriented formatting
========================
:class:`~twiggy.formats.LineFormat` formats messages for text-oriented outputs such as a file or standard error.

.. autoclass:: twiggy.formats.LineFormat
    :noindex:

.. _folding-exceptions:

Using ``'\\n'`` as a traceback prefix will fold exceptions into a single line.

LineFormat uses a `ConversionTable` to stringify the arbitrary fields in a message. To customize, copy the default :data:`~twiggy.formats.line_format` and modify:

.. testcode::

    # in your twiggy_setup
    import copy
    my_format = copy.copy(formats.line_format)
    my_format.conversion.add(key = 'address', # name of the field
                             convertValue = hex, # gets original value
                             convertItem = "{0}={1}".format, # gets called with: key, converted_value
                             required = True)

    # output messages with name 'memory' to stderr
    addEmitters(('memory', levels.DEBUG, filters.names('memory'),
                 outputs.StreamOutput(format = my_format))

For more, refer to the documentation for :class:`ConversionTable`.

***************************
Filtering Output
***************************
The messages output by an emitter are determined by its ``min_level`` and ``filter``. These attributes may be changed while the application is running. The filter attribute of emitters is intelligent; you may assign strings, bools or functions and it will magically do the right thing.  Assigning a list indicates that *all* of the filters must pass for the message to be output.

.. testcode::

    e = emitters['memory']
    e.min_level = levels.WARNING
    # True allows all messages through (None works as well)
    e.fitler = True
    # False blocks all messages
    e.filter = False
    # Strings are interpreted as regexes (regex objects ok too)
    e.filter = "^mem.*y$"
    # functions are passed the message; return True to emit
    e.filter = lambda msg: msg.fields['address'] > 0xDECAF
    # lists are all()'d
    e.filter = ["^mem.y$", lambda msg: msg.fields['address'] > 0xDECAF]

For more see :mod:`~twiggy.filters`
