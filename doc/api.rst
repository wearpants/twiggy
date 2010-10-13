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

*************************
Converter
*************************
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

.. function:: filter(msg) -> bool

    A *filter* is any function that takes a :class:`.Message` and returns True if it should be :class:`emitted <Emitter>`.
    
    :arg `.Message` msg: the message to test

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
.. automodule:: twiggy.logger
    :members:

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
