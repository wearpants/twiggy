######################
Configuring Output
######################

.. currentmodule:: twiggy

This part discusses how to configure twiggy's output of messages.  You should do this once, near the
start of your application's ``__main__``.  It's particularly important to set up Twiggy *before
spawning new processes*.

.. _quick-setup:

*******************
Quick Setup
*******************

:func:`quick_setup` quickly configures output with reasonable defaults. Use it when you don't need
a lot of customizability or as the default configuration that the user can override via
programatic configuration or :ref:`dict_config`.

The defaults will emit log messages of ``DEBUG`` level or higher to ``stderr``:

.. testcode:: quick-setup

    from twiggy import quick_setup
    quick_setup()

.. seealso:: The API docs for complete information on :func:`quick_setup`'s parameters.


.. _twiggy-setup:

*******************
twiggy_setup.py
*******************
.. testsetup:: twiggy-setup

    from twiggy import emitters
    emitters.clear()

Twiggy's output side features modern, loosely coupled design.  The easiest way to understand what
that means is to look at how to configure twiggy programmatically.

.. note::
    Prior to Twiggy 0.5, by convention twiggy was programmatically set up in a separate file in your
    application called ``twiggy_setup.py`` in a function called ``twiggy_setup()``.  This allowed
    sites to override the configuration via their configuration management systems by replacing the
    file.  In Twiggy 0.5 and later, the :ref:`dict_config` function provides a more natural way
    for to allow users to override the logging configuration using a config file.

Programmatically configuring Twiggy involves creating an :ref:`output <outputs>` which defines where the log
messages will be sent and then creating an :class:`.Emitter` which associates a subset of your
application's logs with the output.  Here's what an example ``twiggy_setup()`` function would look
like:

.. testcode:: twiggy-setup

    from twiggy import add_emitters, outputs, levels, filters, formats, emitters # import * is also ok
    def twiggy_setup():
        alice_output = outputs.FileOutput("alice.log", format=formats.line_format)
        bob_output = outputs.FileOutput("bob.log", format=formats.line_format)

        add_emitters(
            # (name, min_level, filter, output),
            ("alice", levels.DEBUG, None, alice_output),
            ("betty", levels.INFO, filters.names("betty"), bob_output),
            ("brian.*", levels.DEBUG, filters.glob_names("brian.*"), bob_output),
            )

    # near the top of your __main__
    twiggy_setup()

In this example, we create two log :ref:`outputs`: ``alice_output`` and ``bob_output``.  These
outputs are :class:`twiggy.outputs.FileOutput`s.  They tell twiggy to write messages directed to
the output into the named file, in this case, ``alice.log`` and ``bob.log``.  All outputs have
a formatter associated with them.  The formatter is responsible for turning Twiggy's
:ref:`structured-logging` calls into a suitable form for the output.  In this example, both
``alice_output`` and ``bob_output`` use :func:`twiggy.formats.line_format` to format their
messages.

:class:`.Emitters` associate :ref:`outputs` with a set of messages via :mod:`.levels` and
:ref:`filters`.  Here we configure three emitters to two outputs.  ``alice_output`` will receive all
messages and ``bob_output`` will receive two sets of messages:

* messages with the name field equal to ``betty`` and level >= ``INFO``
* messages with the name field glob-matching ``brian.*``

The convenience function, :func:`add_emitters`, takes the emitter information as a tuple of emitter
name, minimum log level, optional filters, and the output that the logs should be written to.  It
creates the :class:`.Emitters` from that information and populates the :data:`emitters` dictionary:

.. doctest:: twiggy-setup

    >>> sorted(emitters.keys())
    ['alice', 'betty', 'brian.*']

:class:`Emitters <.Emitter>` can be removed by deleting them from this dict. :attr:`~.Emitter.filter` and :attr:`~.Emitter.min_level` may be modified during the running of the application, but outputs *cannot* be changed.  Instead, remove the emitter and re-add it.

.. doctest:: twiggy-setup

    >>> # bump level
    ... emitters['alice'].min_level = levels.WARNING
    >>> # change filter
    ... emitters['alice'].filter = filters.names('alice', 'andy')
    >>> # remove entirely
    ... del emitters['alice']

We'll examine the various parts in more detail below.

.. note:: Remember to import and run ``twiggy_setup`` near the top of your application.


.. _outputs:

**************************
Outputs
**************************
Outputs are the destinations to which log messages are written (files, databases, etc.). Several :mod:`implementations <.outputs>` are provided. Once created, outputs cannot be modified.  Each output has an associated :mod:`format <.formats>`.

.. _async-logging:

Asynchronous Logging
====================
Many outputs can be configured to use a separate, dedicated process to log messages. This is known as :term:`asynchronous logging` and is enabled with the `msg_buffer <.AsyncOutput>` argument. Asynchronous mode dramatically reduces the cost of logging, as expensive formatting and writing operations are moved out of the main thread of control.

.. warning: There is a slight, but non-zero, chance that messages may be lost if something goes awry with the child process.

.. _formats:

*********************
Formats
*********************
:mod:`Formats <.formats>` transform a log message into a form that can be written by an output. The result of formatting is output dependent; for example, an output that posts to an HTTP server may take a format that provides JSON, whereas an output that writes to a file may produce text.

Line-oriented formatting
========================
:class:`.LineFormat` formats messages for text-oriented outputs such as a file or standard error. It uses a `.ConversionTable` to stringify the arbitrary fields in a message. To customize, copy the default :data:`.line_format` and modify:

.. testsetup:: line-format

    from twiggy import *
    emitters.clear()

.. testcode:: line-format

    # in your twiggy_setup
    import copy
    my_format = copy.copy(formats.line_format)
    my_format.conversion.add(key = 'address', # name of the field
                             convert_value = hex, # gets original value
                             convert_item = "{0}={1}".format, # gets called with: key, converted_value
                             required = True)

    # output messages with name 'memory' to stderr
    add_emitters(('memory', levels.DEBUG, filters.names('memory'), outputs.StreamOutput(format = my_format)))


.. _filters:

***************************
Filtering Output
***************************
The messages output by an emitter are determined by its :attr:`~.Emitter.min_level` and filter (a :func:`function <.filter>` which take a :class:`.Message` and returns bool). These attributes may be changed while the application is running. The :attr:`~.Emitter.filter` attribute of emitters is `intelligent <.msg_filter>`; you may assign strings, bools or functions and it will magically do the right thing.  Assigning a list indicates that *all* of the filters must pass for the message to be output.

.. testcode:: line-format

    e = emitters['memory']
    e.min_level = levels.WARNING
    # True allows all messages through (None works as well)
    e.filter = True
    # False blocks all messages
    e.filter = False
    # Strings are interpreted as regexes (regex objects ok too)
    e.filter = "^mem.*y$"
    # functions are passed the message; return True to emit
    e.filter = lambda msg: msg.fields['address'] > 0xDECAF
    # lists are all()'d
    e.filter = ["^mem.y$", lambda msg: msg.fields['address'] > 0xDECAF]

.. seealso:: Available :mod:`.filters`


.. _dict_config:

*******************
dict_config()
*******************
.. testsetup:: dict_config

    from twiggy import emitters
    emitters.clear()

Twiggy 0.5 features a new convenience method, :func:`.dict_config` for configuring
:class:`Emitters <.Emitter>` that takes a a dictionary with the configuration information. The
dictionary can be constructed programmatically, loaded from a configuration file, or hardcoded
into an application. This allows the programmer to easily set defaults and allow the user to
override those from a configuration file. Here's an example:

.. testcode:: dict_config

    from twiggy import dict_config

    twiggy_config = {'version': '1.0',
                     'outputs': {
                        'alice_output': {
                            'output': 'twiggy.outputs.FileOutput',
                            'args': ['alice.log']
                        },
                        'bob_output': {
                            'output': 'twiggy.outputs.FileOutput',
                            'args': ['bob.log'],
                            'format': 'twiggy.formats.line_format'
                        }
                     },
                     'emitters': {
                        'alice': {
                            'level': 'DEBUG',
                            'output_name': 'alice_output'
                        },
                        'betty': {
                            'level': 'INFO',
                            'filters': [ {
                                'filter': 'twiggy.filters.names',
                                'args': ['betty']
                                }
                            ],
                            'output_name': 'bob_output'
                        },
                        'brian.*': {
                            'level': 'DEBUG',
                            'filters': [ {
                                'filter': 'twiggy.filters.glob_names',
                                'args': ['brian.*']
                                }
                            ],
                            'output_name': 'bob_output'
                        }
                    }
                }

    dict_config(twiggy_config)

In this example, the programmer creates a twiggy configuration in the application's code and uses it
to configure twiggy.  The configuration closely mirrors the objects that were created in the
:ref:`twiggy-setup` section.  The ``outputs`` field contains definitions of ``alice_output`` and
``bob_output`` that write to the ``alice.log`` and ``bob.log`` files respectively.  The ``emitters``
field defines three emitters, their levels and filters to output to the

The configuration should be done near the start of your application.  It's
particularly important to set up Twiggy *before spawning new processes*.

With this configuration, :func:`twiggy.dict_config` will create two log destinations (:ref:`outputs`):
``alice.log`` and ``bob.log``.  These :ref:`outputs` are  then associated with the set of messages
that they will receive in the ``emitters`` section.  :file:`alice.log` will receive all messages and
:file:`bob.log` will receive two sets of messages:

* messages with the name field equal to ``betty`` and level >= ``INFO``
* messages with the name field glob-matching ``brian.*``

See the :ref:`twiggy_config_schema` documentation for details of what each of the fields in the
configuration dictionary mean.


User Overrides
==============

Each site that runs an application is likely to have different logging needs. Using
`dict_config` it is easy to let the user override the configuration specified by the program. For
instance, the application could have a yaml configuration file with a ``logging_config`` section::

    import yaml
    config = yaml.safe_load('config_file.yml')
    if 'logging_config' in config:
        try:
            twiggy.dict_config(config['logging_config'])
        except Exception as e:
            print('User provided logging configuration was flawed: {0}'.format(e))


.. _twiggy_config_schema:

Twiggy Config Schema
====================

The dict taken by :func:`twiggy.dict_config` may contain the following keys:

version
    Set to the value representing the schema version as a string.  Currently, the only valid value
    is "1.0".

incremental
    (*Optional*) If True, the dictionary will update any existing configuration.  If False, this
    will override any existing configuration.  This allows user defined logging configuration to
    decide whether to override the logging configuration set be the application or merely supplement
    it.  The default is False.

outputs
    (*Optional*) Mapping of output names to outputs. Outputs consist of

    output
        A :class:`twiggy.outputs.Output` or the string representation with which to import
        a :class:`~twiggy.outputs.Output`.  For instance, to use the builtin,
        :class:`twiggy.outputs.FileOutput` either set output directly to the class or the string
        ``twiggy.outputs.FileOutput``.

    args
        (*Optional*) A list of arguments to pass to the :class:`Twiggy.outputs.Output` class
        constructor.  For instance, :class:`~twiggy.outputs.FileOutput` takes the filename of a file
        to log to.  So ``args`` could be set to: ``["logfile.log"]``.

    kwargs
        (*Optional*) A dict of keyword arguments to pass to the :class:`Twiggy.outputs.Output` class
        constructor.  For instance, :class:`~twiggy.outputs.StreamOutput` takes a stream as
        a keyword argument so ``kwargs`` could be set to: ``{"stream": "ext://sys.stdout"}``.

    format
        (*Optional*) A formatter function which transforms the log message for the output.  This can
        either be a string name of the formatter of the formatter itself. The default is
        :func:`twiggy.formats.line_format`

    If both ``outputs`` and ``emitters`` are None and `incremental` is False then
    :data:`twiggy.emitters` will be cleared.

emitters
    (*Optional*) Mapping of emitter names to emitters.  Emitters consist of:

    level
        String name of the log level at which log messages will be passed to this emitter.
        May be one of (In order of severity) ``CRITICAL``, ``ERROR``, ``WARNING``, ``NOTICE``,
        ``INFO``, ``DEBUG``, ``DISABLED``.

    output_name
        The name of an output in this configuration dict.

    filters
        (*Optional*) A list of filters which filter out messages which will go to this emitter.
        Each filter is a mapping which consists of:

        filter
            Name for a twiggy filter function.  This can either be a string name for the function or
            the function itself.

        args
            (*Optional*) A list of arguments to pass to the :class:`Twiggy.outputs.Output` class
            constructor.  For instance, :class:`~twiggy.outputs.FileOutput` takes the filename of a file
            to log to.  So ``args`` could be set to: ``["logfile.log"]``.

        kwargs
            (*Optional*) A dict of keyword arguments to pass to the :class:`Twiggy.outputs.Output` class
            constructor.  For instance, :class:`~twiggy.outputs.StreamOutput` takes a stream as
            a keyword argument so ``kwargs`` could be set to: ``{"stream": "ext://sys.stdout"}``.

    If both ``emitters`` and ``output`` are None and `incremental` is False then
    :data:`twiggy.emitters` will be cleared.

Sometimes you want to have an entry in ``args`` or ``kwargs`` that is a python object. For
instance, :class:`~twiggy.outputs.StreamOutput` takes a stream keyword argument so you may want to
give ``sys.stdout`` to it. If you are building the configuration dictionary in Python code you can
simply use the actual object. However, if you are writing in a text configuration file, you can
specify existing objects by prefixing the string with ``ext://``. When Twiggy sees that the string
starts with ``ext://`` it will strip off the prefix and then try to import an object with the rest
of the name.

Here's an example config that you might find in a YAML config file:

.. code-block:: yaml

    version: '1.0'
    outputs:
        alice_output:
            output: 'twiggy.outputs.FileOutput'
            args:
                - 'alice.log'
        bob_output:
            output: 'twiggy.outputs.StreamOutput'
            kwargs:
                stream: 'ext://sys.stdout'
            format: 'twiggy.formats.line_format'
    emitters:
        alice:
            level: 'DEBUG'
            output_name: 'alice_output'
        betty:
            level: 'INFO'
            filters:
                filter: 'twiggy.filters.names'
                args:
                    - 'betty'
            output_name: 'bob_output'
        brian.*:
            levels: 'DEBUG'
            filters:
                filter: 'twiggy.filters.glob_names'
                args:
                    -'brian.*'
            output_name: 'bob_output'
