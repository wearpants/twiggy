Twiggy
=================================

.. image:: https://pypip.in/version/twiggy/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/twiggy/
    :alt: Latest Version
    
.. image:: https://img.shields.io/travis/wearpants/twiggy.svg
    :target: https://travis-ci.org/wearpants/twiggy

Twiggy is a Pythonic logger.

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
`documentation <http://twiggy.wearpants.org>`_ or `see this blog post
<http://blog.wearpants.org/meet-twiggy>`_.

Note that `master` is currently in flux and may be broken. Please use the
maint-0.4_ branch for stable development/forks.

.. _maint-0.4: https://github.com/wearpants/twiggy/tree/maint-0.4
