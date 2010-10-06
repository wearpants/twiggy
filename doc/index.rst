.. Twiggy documentation master file, created by
   sphinx-quickstart on Mon Sep 20 10:33:48 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################################
The Story of Twiggy!
##################################
Twiggy was born at Pycon 2010.

.. seealso:: :doc:`blog_post_notes`

Twiggy is awesome::

    >>> log.name('frank').fields(number=42).info("hello {who}, it's a {} day", 'sunny', who='world')
    INFO:frank:number=42:hello world, it's a sunny day

*******************
Why Logging Matters
*******************
* your **only** view into a running program
* your **only** view of past execution
* your **data** for post-mortem & domain-specific measurement

Contents:

.. toctree::
    :maxdepth: 2
    :glob:

    intro
    basic_use
    configuration
    reference_guide
    api
    glossary


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
