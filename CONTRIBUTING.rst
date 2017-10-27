============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/wearpants/twiggy/issues

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs & Implement Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for bugs & enhancements. Anything tagged "help wanted" is a good place to start.
If you'd like to work on a different issue, don't hesitate to ask!


Write Documentation
~~~~~~~~~~~~~~~~~~~

Twiggy could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/twiggy/wearpants/issues.

If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `twiggy` for local development. Please note this documentation assumes
you already have `virtualenv` and `Git` installed and ready to go.

1. Fork the `twiggy` repo on GitHub.
2. Clone your fork locally::

  .. code-block:: bash

    $ cd path_for_the_repo
    $ git clone git@github.com:YOUR_NAME/twiggy.git

3. Assuming you have virtualenv installed (If you have Python3.5 this should already be there), you can create a new environment for your local development by typing::

  .. code-block:: bash

    $ virtualenv twiggy-env
    $ source twiggy-env/bin/activate

    This should change the shell to look something like
    (twiggy-env) $

4. Create a branch for local development::

  .. code-block:: bash

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8::

  .. code-block:: bash

    $ flake8

6. The next step would be to run the test cases. `twiggy` uses py.test, you can run PyTest. Before you run pytest you should ensure all dependancies are installed::

  .. code-block:: bash

    $ pip install -r test-requirements.txt
    $ py.test ./tests

7. Before raising a pull request you should also run tox. This will run the tests across different versions of Python::

  .. code-block:: bash

    $ tox

   .. note::
      If you are missing flake8, pytest and/or tox, just pip install them into your virtualenv.

8. If your contribution is a bug fix or new feature, you may want to add a test to the existing test suite. See section Add a New Test below for details. 

9. Commit your changes and push your branch to GitHub::

  .. code-block:: bash

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

10. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.

3. The pull request should work for Python 2.7, 3.3, 3.4, 3.5 & 3.6, and for PyPy 2 and 3. Check
   https://travis-ci.org/weapants/twiggy/pull_requests
   and make sure that the tests pass for all supported Python versions.

Add a New Test
---------------
When fixing a bug or adding features, it's good practice to add a test to demonstrate your fix or new feature behaves as expected. These tests should focus on one tiny bit of functionality and prove changes are correct. 

To write and run your new test, follow these steps:

1. Add the new test to `tests/test_new_thing.py`. Focus your test on the specific bug or a small part of the new feature. 

2. If you have already made changes to the code, stash your changes and confirm all your changes were stashed::
  
    $ git stash
    $ git stash list

3. Run your test and confirm that your test fails. If your test does not fail, rewrite the test until it fails on the original code::

    $ py.test ./tests

4. (Optional) Run the tests with tox to ensure that the code changes work with different Python versions::

    $ tox

5. Proceed work on your bug fix or new feature or restore your changes. To restore your stashed changes and confirm their restoration::

    $ git stash pop
    $ git stash list

6. Rerun your test and confirm that your test passes. If it passes, congratulations!

.. twiggy: https://github.com/weapants/twiggy
.. virtualenv: https://virtualenv.pypa.io/en/stable/installation
.. git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
