#!/usr/bin/env python

from distutils.core import setup

setup(name='Twiggy',
      version='0.2',
      description='Twiggy is a more Pythonic logger',
      author='Peter Fein',
      author_email='pfein@pobox.com',
      url='http://python-twiggy.googlecode.com',
      download_url='http://python-twiggy.googlecode.com/files/Twiggy-0.2.tar.gz',
      packages=['twiggy', 'twiggy.lib'],
      long_description=file('notes.txt').read(),
      license = "BSD",
      classifiers = [
      "Topic :: System :: Logging",
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: BSD License",]
      )
