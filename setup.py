#!/usr/bin/env python

from distutils.core import setup
import os.path
import sys

# stop with the bug reports
if sys.version_info < (2, 6):
    raise RuntimeError("Twiggy requires Python 2.6 or greater")

# this horrible mess brought to you by the crap that is Python distutils. Just use CPAN.
version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
VERSION = open(version_file).read().strip().split('.')
release = '.'.join(VERSION)

setup(name='Twiggy',
      version=release,
      description='a Pythonic logger',
      author='Pete Fein',
      author_email='pete@wearpants.org',
      url='http://twiggy.wearpants.org',
      packages=['twiggy', 'twiggy.lib', 'twiggy.features'],
      license = "BSD",
      classifiers = [
      "Topic :: System :: Logging",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: BSD License",],
      long_description=open('README.rst').read(),
      )
