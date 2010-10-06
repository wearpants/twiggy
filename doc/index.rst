.. Twiggy documentation master file, created by
   sphinx-quickstart on Mon Sep 20 10:33:48 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################################
Twiggy: A Pythonic Logger
##################################
Twiggy is a more Pythonic logger.

    >>> log.name('frank').fields(number=42).info("hello {who}, it's a {} day", 'sunny', who='world')
    INFO:frank:number=42:hello world, it's a sunny day

****************************
Who, What, When, Where, Why
****************************

:author: Peter Fein
:email: pfein@pobox.com
:homepage: http://python-twiggy.googlecode.com/

Twiggy was born at `Pycon 2010 <http://us.pycon.org/2010/>`_ after I whined about the standard library's `logging <http://docs.python.org/library/logging.html>`_ and Jesse Noller "invited" me to do something about it.

Get it from the `Cheeseshop <http://pypi.python.org/pypi/Twiggy>`_::

    pip install Twiggy

    easy_install -U Twiggy

Why Logging Matters
===================
Logging is:

* your **only** view into a running program
* your **only** view of past execution
* your **data** for post-mortem & domain-specific measurement

Why Twiggy Should Be Your New Logger
====================================

You should use Twiggy because it is awesome.

* lighter
* friendlier
* safer
* faster
* cooler
* more fun
* not boring

.. warning::
    Twiggy is beta software; do not use for nuclear power plants, spaceships or mortgage derivatives trading (not that it'd matter).

.. seealso:: :doc:`blog_post_notes`

***********
Contents
***********
.. toctree::
    :maxdepth: 2
    :glob:

    logging
    configuration
    reference_guide
    api
    glossary


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
