######################
Testing
######################

.. currentmodule:: twiggy

This part discusses how to test Twiggy to ensure that Twiggy is built and installed correctly.

*******************
Requirements
*******************
The following need to be installed prior to testing:

* Python 2.7.1 or greater.

* The `coverage <http://pypi.python.org/pypi/coverage>`_ module.

* `sphinx <http://sphinx.pocoo.org/>`_ 1.0.8 or greater. You'll need to get and build the `sphinx source <https://bitbucket.org/birkenfeld/sphinx/>`_.

* `Twiggy source <http://hg.wearpants.org/twiggy/>`_.

*******************
Running Tests
*******************
Note: Tests **must** be run from the Twiggy root directory to work.

To run all tests (unittest and Sphinx doctests)::

    ./scripts/run-twiggy-tests.sh

To run coverage tests, run::

    ./scripts/cover-twiggy-tests.sh discover -b

To run coverage tests on a specific module, run::

    ./scripts/cover-twiggy-tests.sh tests.test_levels
