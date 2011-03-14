"""
This module allows replacing stdlib's logging module with twiggy,
it implements the following interface:

  getLogger - returns a logger that supports debug/info/error etc'.
  root - the root logger, or just 'log' in twiggy.
"""
__all__ = ['hijack', 'restore', 'hijack_context', # patching
           'getLogger', 'root'] # API

import sys
import logging as orig_logging
from twiggy import log
from twiggy.levels import *
from contextlib import contextmanager

def hijack():
    """Replace the original module with the compatibility module."""
    sys.modules['logging'] = sys.modules[__name__]

def restore():
    """Replace the compatibility module with the original module."""
    sys.modules['logging'] = orig_logging

@contextmanager
def hijack_context():
    """Hijack and finally restore."""
    hijack()
    try:
        yield
    finally:
        restore()

def forward(s):
    def method(self, *args, **kwargs):
        return getattr(self._logger, s)(*args, **kwargs)
    return method

class FakeLogger(object):
    
    __slots__ = ["_logger"]

    def __init__(self, logger):
        self._logger = logger

    debug = forward("debug")
    info = forward("info")
    warn = warning = forward("debug")
    error = forward("error")
    critical = forward("critical")
    
    def setLevel(self, level):
        self._logger.min_level = level

    def log(self, level, format_spec, *args, **kwargs):
        logger = self._logger
        if kwargs.pop("exc_info", False):
            logger = logger.trace("error")
        if not isinstance(level, levels.LogLevel):
            raise ValueError("Unknown level: {0}".format(level))
        logger._emit(level, format_spec, args, kwargs)

root = FakeLogger(log.options(style='percent'))

_logger_cache = {} # name to logger
def getLogger(name=None):
    if name is not None:
        if name not in logger_cache:
            _logger_cache[name] = FakeLogger(log.name(name).options(style='percent'))
        return _logger_cache[name]
    return root

