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

Twiggy is a more Pythonic logger.

.. doctest:: demo

    >>> from twiggy import quick_setup, log
    >>> quick_setup()
    >>> log.name('frank').fields(number=42).info("hello {who}, it's a {0} day", 'sunny', who='world')
    INFO:frank:number=42:hello world, it's a sunny day

:author: `Peter Fein <http://i.wearpants.org>`_
:email: pete@wearpants.org
:twitter: `@petecode <https://twitter.com/petecode>`_
:homepage: http://twiggy.wearpants.org/
:hosting: https://github.com/wearpants/twiggy
:IRC: `irc://irc.freenode.net/#twiggy <http://irc.lc/freenode/twiggy/>`_
:license: `BSD <http://www.opensource.org/licenses/bsd-license.php>`_
:Python: 2.6, 2.7

Twiggy was born at `Pycon 2010 <http://us.pycon.org/2010/>`_ after I whined about the standard library's `logging <http://docs.python.org/library/logging.html>`_ and Jesse Noller "invited" me to do something about it.

Install straight with distutils from the `Cheeseshop <http://pypi.python.org/pypi/Twiggy>`_ or::

    pip install Twiggy

    easy_install -U Twiggy

Get the latest version::

    git clone https://github.com/wearpants/twiggy.git

*************************************
Why Twiggy Should Be Your New Logger
*************************************

You should use Twiggy because it is awesome. For more information, `see this blog post <http://blog.wearpants.org/meet-twiggy>`_.

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
