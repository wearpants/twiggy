.. Twiggy documentation master file, created by
   sphinx-quickstart on Mon Sep 20 10:33:48 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################################
Twiggy: A Pythonic Logger
##################################

****************************
Who, What, When, Where
****************************

Twiggy is a more Pythonic logger.  It aims to be easy to setup:

.. doctest::

    >>> from twiggy import quick_setup
    >>> quick_setup()

And fun to use!

.. doctest:: demo

    >>> from twiggy import log
    >>> log.name('frank').fields(number=42).info("hello {who}, it's a {0} day", 'sunny', who='world')
    INFO:frank:number=42|hello world, it's a sunny day

:author: `Peter Fein <https://wearpants.org/about>`_
:email: pete@wearpants.org
:twitter: `@petecode <https://twitter.com/petecode>`_
:homepage: http://twiggy.readthedocs.io/en/latest/
:hosting: https://github.com/wearpants/twiggy
:IRC: `irc://irc.freenode.net/#twiggy <http://irc.lc/freenode/twiggy/>`_
:license: `BSD <https://opensource.org/licenses/bsd-license.php>`_
:Python: 2.6, 2.7

Twiggy was born at `Pycon 2010 <http://pyvideo.org/events/pycon-us-2010.html>`_ after I whined about the standard library's `logging <https://docs.python.org/3/library/logging.html>`_ and Jesse Noller "invited" me to do something about it.

Install straight with distutils from the `Cheeseshop <https://pypi.python.org/pypi/Twiggy>`_ or::

    pip install Twiggy

    easy_install -U Twiggy

Get the latest version::

    git clone https://github.com/wearpants/twiggy.git

*************************************
Why Twiggy Should Be Your New Logger
*************************************

You should use Twiggy because it is awesome. For more information, `see this blog post <https://wearpants.org/petecode/meet-twiggy/>`_.

.. warning::
    Twiggy works great, but is not rock solid (yet); do not use for nuclear power plants, spaceships or mortgage derivatives trading (not that it'd matter).

**************
Documentation
**************
.. toctree::
    :maxdepth: 2
    :glob:

    logging
    configuration
    reference_guide
    api
    testing
    glossary
    changelog
    contributors
