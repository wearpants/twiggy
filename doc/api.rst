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

    the global :class:`emitters <.Emitter>` dictionary

.. autofunction:: addEmitters

.. autofunction:: quickSetup


*************************
Library
*************************
.. automodule:: twiggy.lib
    :members:

Converter
===============
.. automodule:: twiggy.lib.converter
    :members:

*************************
Features
*************************

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

.. autoclass:: Emitter

*************************
Formats
*************************
.. automodule:: twiggy.formats
    :members:

*************************
Levels
*************************
.. automodule:: twiggy.levels
    :members:

*************************
Logger
*************************
Loggers should not be created directly by users; use the global :data:`.log` instead.

.. module:: twiggy.logger
    
.. class:: BaseLogger

    Base class for loggers

    .. attribute:: _fields
    
        dictionary of bound fields for :term:`structured logging`.

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
    
    The following methods cause messages to be emitted.  ``format_spec`` is a template string into which ``args`` and ``kwargs`` will be substitued.
    
    .. automethod:: debug
    .. automethod:: info
    .. automethod:: warning
    .. automethod:: error
    .. automethod:: critical


.. class:: Logger
    
    Logger for end-users. The type of the magic :data:`.log`
    
    .. attribute:: filter
    
        Filter on ``format_spec``. For optimization purposes only. Should have the following signature:
        
        .. function:: func(format_spec : string) -> bool
            :noindex:
            
            Should the message be emitted.
        

.. autoclass:: InternalLogger

.. autofunction:: emit

*************************
Message
*************************
.. automodule:: twiggy.message
    :members:

*************************
Outputs
*************************
.. automodule:: twiggy.outputs
    :members:
