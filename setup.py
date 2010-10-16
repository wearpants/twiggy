#!/usr/bin/env python

from distutils.core import setup

setup(name='Twiggy',
      version='0.4.0',
      description='a Pythonic logger',
      author='Peter Fein',
      author_email='pfein@pobox.com',
      url='http://twiggy.wearpants.org',
      download_url='http://python-twiggy.googlecode.com/files/Twiggy-0.4.0.tar.gz',
      packages=['twiggy', 'twiggy.lib', 'twiggy.features'],
      license = "BSD",
      classifiers = [
      "Topic :: System :: Logging",
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: BSD License",],
      long_description=open('README').read(),
      )
