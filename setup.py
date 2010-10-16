#!/usr/bin/env python

from distutils.core import setup

setup(name='Twiggy',
      version='0.4',
      description='a Pythonic logger',
      author='Peter Fein',
      author_email='pfein@pobox.com',
      url='http://twiggy.wearpants.org',
      download_url='http://python-twiggy.googlecode.com/files/Twiggy-0.4.tar.gz',
      packages=['twiggy', 'twiggy.lib', 'twiggy.features'],
      license = "BSD",
      classifiers = [
      "Topic :: System :: Logging",
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: BSD License",],
      long_description="""Twiggy is a Pythonic logger
      
>>> log.name('frank').fields(number=42).info("hello {who}, it's a {} day", 'sunny', who='world')
INFO:frank:number=42:hello world, it's a sunny day

You should use Twiggy because it is awesome. For more information, `see this blog post <http://blog.wearpants.org/meet-twiggy>`_ or the `project homepage <http://twiggy.wearpants.org>`_.
"""
)
