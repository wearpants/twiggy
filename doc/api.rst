#########################
API Reference
#########################

*************************
Global Objects
*************************
.. module:: twiggy

.. data:: log

    the magic log object

.. data:: internal_log

    `.InternalLogger` for reporting errors within Twiggy itself

.. data:: devel_log

    `.InternalLogger` for use by developers writing extensions to Twiggy

.. data:: emitters

    the global :class:`emitters <.Emitter>` dictionary, tied to the :data:`.log`

.. autofunction:: addEmitters

.. autofunction:: quickSetup

*************************
Features
*************************

.. automodule:: twiggy.features
    :members:

procinfo
===========
.. automodule:: twiggy.features.procinfo
    :members:

socket
========
.. automodule:: twiggy.features.socket
    :members:

*************************
Filters
*************************
.. module:: twiggy.filters

.. function:: filter(msg : Message) -> bool

    A *filter* is any function that takes a :class:`.Message` and returns True if it should be :class:`emitted <Emitter>`.

.. function:: msgFilter(x) -> filter

    create a `.filter` intelligently

    You may pass:

        :None, True: the filter will always return True
        :False: the filter will always return False
        :string: compiled into a regex
        :regex: ``match()`` against the message text
        :callable: returned as is
        :list: apply `msgFilter` to each element, and ``all()`` the results

    :rtype: `.filter` function

.. function:: names(*names) -> filter

    create a `.filter`, which gives True if the messsage's name equals any of those provided

    ``names`` will be stored as an attribute on the filter.

    :arg strings names: names to match
    :rtype: `.filter` function

.. function:: glob_names(*names) -> filter

    create a `.filter`, which gives True if the messsage's name globs those provided.

    ``names`` will be stored as an attribute on the filter.

    This is probably quite a bit slower than :func:`names`.

    :arg strings names: glob patterns.
    :rtype: `.filter` function

.. class:: Emitter

    Hold and manage an :class:`.Output` and associated :func:`.filter`

    .. attribute:: min_level

        only emit if greater than this `.LogLevel`

    .. attribute:: filter

        arbitrary :func:`.filter` on message contents. Assigning to this attribute is :func:`intelligent <.msgFilter>`.

    .. attribute:: _output

        `.Output` to emit messages to. Do not modify.

*************************
Formats
*************************

.. module:: twiggy.formats

.. _format-function:

*Formats* are single-argument callables that take a `.Message` and return an object appropriate for the `.Output` they are assigned to.

.. class:: LineFormat(separator=':', traceback_prefix='\\nTRACE', conversion=line_conversion)


    .. attribute:: separator

        string to separate line parts. Defaults to ``:``.

    .. attribute:: traceback_prefix

        string to prepend to traceback lines. Defaults to ``\nTRACE``.

        .. _folding-exceptions:

        Set to ``'\\n'`` (double backslash n) to roll up tracebacks to a single line.

    .. attribute:: conversion

        :class:`.ConversionTable` used to format :attr:`.fields`. Defaults to :data:`line_conversion`

    .. automethod:: format_text

    .. automethod:: format_fields

    .. automethod:: format_traceback


.. data:: line_conversion

    a default line-oriented :class:`.ConversionTable`. Produces a nice-looking string from :attr:`.fields`.

    Fields are separated by a colon (``:``). Resultant string includes:

        :time: in iso8601 format (required)
        :level: message level (required)
        :name: logger name

    Remaining fields are sorted alphabetically and formatted as ``key=value``

.. data:: line_format

    a default :class:`.LineFormat` for output to a file. :ref:`Sample output <sample-file-output>`.

    Fields are formatted using :data:`.line_conversion` and separated from the message :attr:`.text` by a colon (``:``). Traceback lines are prefixed by ``TRACE``.

.. data:: shell_conversion

    a default line-oriented :class:`.ConversionTable` for use in the shell.  Returns the same string as :data:`.line_conversion` but drops the ``time`` field.

.. data:: shell_format

    a default :class:`.LineFormat` for use in the shell.  Same as :data:`.line_format` but uses :data:`.shell_conversion` for :attr:`.fields`.

*************************
Levels
*************************
.. automodule:: twiggy.levels
    :members:

*************************
Library
*************************
.. automodule:: twiggy.lib
    :members:

Converter
===============
.. module:: twiggy.lib.converter

.. autoclass:: Converter

.. class:: ConversionTable(seq)

    Convert data dictionaries using `Converters <.Converter>`

    For each item in the dictionary to be converted:

    #. Find one or more corresponding converters ``c`` by matching key.
    #. Build a list of converted items by calling ``c.convertItem(item_key, c.convertValue(item_value))``. The list will have items in the same order as converters were supplied.
    #. Dict items for which no converter was found are sorted by key and passed to `.genericValue` / `.genericItem`. These items are appended to the list from step 2.
    #. If any required items are missing, :exc:`ValueError` is raised.
    #. The resulting list of converted items is passed to `.aggregate`. The value it returns is the result of the conversion.


    Users may override `.genericValue`/`.genericItem`/`.aggregate` by subclassing or assigning a new function on a ConversionTable instance.

    Really, it's :ref:`pretty intuitive <conversion-table-example>`.

    .. automethod:: __init__

    .. automethod:: convert

    .. method:: genericValue(value)

        convert values for which no specific `.Converter` is supplied

    .. method:: genericItem(key, value)

        convert items for which no specific `.Converter` is supplied

    .. method:: aggregate(converteds)

        aggregate list of converted items.  The return value of `.convert`

    .. automethod:: copy

    .. automethod:: get

    .. automethod:: getAll

    .. automethod:: add

    .. automethod:: delete


*************************
Logger
*************************
Loggers should not be created directly by users; use the global :data:`.log` instead.

.. module:: twiggy.logger

.. class:: BaseLogger(fields=None, options=None, min_level=None)

    Base class for loggers

    .. attribute:: _fields

        dictionary of bound fields for :term:`structured logging`.
        By default, contains a single field ``time`` with value ``time.gmtime()``.  This function will be called for each message emitted, populating the field with the current ``time.struct_time``.

    .. attribute:: _options

        dictionary of bound :ref:`options <message-options>`.

    .. attribute:: min_level

        minimum :class:`.LogLevel` for which to emit. For optimization purposes only.

    .. method:: fields(**kwargs) -> bound Logger

        bind fields for :term:`structured logging`. ``kwargs`` are interpreted as names/values of fields.

    .. method:: fieldsDict(d) -> bound Logger

        bind fields for structured logging. Use this instead of `.fields` if you have keys which are not valid Python identifiers.

        :arg dict d: dictionary of fields. Keys should be strings.

    .. method:: options(**kwargs) -> bound Logger

        bind :ref:`options <message-options>` for message creation.

    .. method:: trace(trace='error') -> bound Logger

        convenience method to enable :ref:`traceback logging <message-options>`

    .. method:: name(name) -> bound Logger

        convenvience method to bind ``name`` field

    .. method:: struct(**kwargs) -> bound Logger

        convenience method for :term:`structured logging`. Calls :meth:`.fields` and emits at `.info`

    .. method:: structDict(d) -> bound Logger

        convenience method for :term:`structured logging`. Use instead of `.struct` if you have keys which are not valid Python identifiers.

        :arg dict d: dictionary of fields. Keys should be strings.



    The following methods cause messages to be emitted.  ``format_spec`` is a template string into which ``args`` and ``kwargs`` will be substitued.

    .. automethod:: debug
    .. automethod:: info
    .. automethod:: warning
    .. automethod:: error
    .. automethod:: critical


.. class:: Logger(fields=None, options=None, min_level=None)

    Logger for end-users. The type of the magic :data:`.log`

    .. attribute:: filter

        Filter on ``format_spec``. For optimization purposes only. Should have the following signature:

        .. function:: func(format_spec : string) -> bool
            :noindex:

            Should the message be emitted.

    .. automethod:: addFeature

    .. automethod:: disableFeature

    .. automethod:: delFeature

.. autoclass:: InternalLogger

.. autofunction:: emit

*************************
Message
*************************
.. module:: twiggy.message

.. class:: Message(level, format_spec, fields, options, args, kwargs)

    A logging message.  Users never create these directly.

    .. versionchanged:: 0.4.1
        Pass args/kwargs as list/dict instead of via ``*``/``**`` expansion.

    .. _message-options:

    The constructor takes a dict of ``options`` to control message creation.  In addition to :attr:`.suppress_newlines`, the following options are recognized:

        :trace: control traceback inclusion.  Either a traceback tuple, or one of the strings ``always``, ``error``, in which case a traceback will be extracted from the current stack frame.
        :style: the style of template used for ``format_spec``. One of ``braces``, ``percent``, ``dollar``.

    Any callables passed in ``fields``, ``args`` or ``kwargs`` will be called and the returned value used instead. See :ref:`dynamic messages <dynamic-messages>`.

    All attributes are read-only.

    .. attribute:: fields

        dictionary of :term:`structured logging` fields.  Keys are string, values are arbitrary. A ``level`` item is required.

    .. attribute:: suppress_newlines

        should newlines be escaped in output. Boolean.

    .. attribute:: traceback

        a stringified traceback, or None.

    .. attribute:: text

        the human-readable message. Constructed by substituting ``args``/``kwargs`` into ``format_spec``. String.

    .. automethod:: __init__


*************************
Outputs
*************************
.. module:: twiggy.outputs

.. class:: Output(format=None, close_atexit=True)

    .. attribute:: _format

        a :ref:`callable <format-function>` taking a `.Message` and formatting it for output. None means return the message unchanged.

    .. attribute:: use_locks

        Class variable, indicating that locks should be used when running in a synchronous, multithreaded environment. Threadsafe subclasses may disable locking for higher throughput. Defaults to True.

    .. automethod:: __init__
    
    .. versionadded:: 0.4.1
        Add the `close_atexit` parameter.     
    
    .. method:: close
        
        Finalize the output.

    The following methods should be implemented by subclasses.

    .. automethod:: twiggy.outputs.Output._open

    .. automethod:: twiggy.outputs.Output._close

    .. automethod:: twiggy.outputs.Output._write

.. class:: AsyncOutput(msg_buffer=0)

    An `.Output` with support for :term:`asynchronous logging`.

    Inheriting from this class transparently adds support for asynchronous logging using the multiprocessing module. This is off by default, as it can cause log messages to be dropped.

    :arg int msg_buffer: number of messages to buffer in memory when using asynchronous logging. ``0`` turns asynchronous output off, a negative integer means an unlimited buffer, a positive integer is the size of the buffer.

.. autoclass:: FileOutput

.. class:: StreamOutput(format, stream=sys.stderr)

    Output to an externally-managed stream.

    The stream will be written to, but otherwise left alone (i.e., it will *not* be closed).

.. autoclass:: NullOutput

.. autoclass:: ListOutput
    
.. versionchanged:: 0.4.1
    Replace `DequeOutput` with more useful `ListOutput`.

