Twiggy
=================================
Twiggy is a Pythonic logger.

.. image:: https://img.shields.io/pypi/v/twiggy.svg
    :target: https://pypi.python.org/pypi/twiggy/
    :alt: Latest Version
    
.. image:: https://img.shields.io/travis/wearpants/twiggy.svg
    :target: https://travis-ci.org/wearpants/twiggy

.. image:: 	https://img.shields.io/readthedocs/twiggy/stable.svg
    :target: http://twiggy.readthedocs.io/en/stable/
    :alt: Documentation
    
 


.. code-block:: pycon

    >>> from twiggy import quick_setup, log
    >>> quick_setup()
    >>> log.name('frank') \
    ...    .fields(number=42) \
    ...    .info('hello {who}, it's a {0} day',
                 'sunny',
                 who='world')
    INFO:frank:number=42:hello world, it's a sunny day

You should use Twiggy because it is awesome. For more information, read the
`documentation <https://twiggy.readthedocs.io/en/latest/>`_ or `see this blog post
<https://snake.dev/blog/meet-twiggy/>`_.
