"""
This module allows replacing stdlib's logging module with twiggy,
it implements the following interface:

getLogger - returns a logger that supports debug/info/error etc'.
root - the root logger, or just 'log' in twiggy.
"""
import sys
import logging as orig_logging
from twiggy import log
from contextlib import contextmanager

def hijack():
    """Replace the original module with the compatibility module."""
    sys.modules['logging'] = sys.modules[__name__]

def restore():
    """Replace the compatibility module with the original module."""
    sys.modules['logging'] = orig_logging

@contextmanager
def hijackContext():
    """Hijack and finally restore."""
    hijack()
    try:
        yield
    finally:
        restore()

def getLogger(name=None):
    if name is not None:
        return log.name(name)
    else:
        return log

root = log
