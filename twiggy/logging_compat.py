"""g
This module allows replacing stdlib's logging module with twiggy,
it implements the following interface:

  getLogger - returns a logger that supports debug/info/error etc'.
  root - the root logger, or just 'log' in twiggy.
"""
__all__ = ["hijack", "restore", "hijack_context", # patching
           "getLogger", "root"] # API

import sys
import logging as orig_logging
from twiggy import log, levels
from twiggy.levels import *
from contextlib import contextmanager

def basicConfig(**kwargs):
    raise RuntimeError("Twiggy doesn't support logging's basicConfig")

def hijack():
    """Replace the original module with the compatibility module."""
    sys.modules["logging"] = sys.modules[__name__]

def restore():
    """Replace the compatibility module with the original module."""
    sys.modules["logging"] = orig_logging

@contextmanager
def hijack_context():
    """Hijack and finally restore."""
    hijack()
    try:
        yield
    finally:
        restore()

def log_func_decorator(level):
    def new_func(self, *args, **kwargs):
        return self.log(level, *args, **kwargs)
    return new_func

class FakeLogger(object):
    
    __slots__ = ["_logger"]

    def __init__(self, logger):
        self._logger = logger

    debug = log_func_decorator(DEBUG)
    info = log_func_decorator(INFO)
    warn = warning = log_func_decorator(WARNING)
    error = log_func_decorator(ERROR)
    critical = log_func_decorator(CRITICAL)
    
    def setLevel(self, level):
        self._logger.min_level = level

    @property
    def level(self):
        return self._logger.min_level

    def log(self, level, format_spec, *args, **kwargs):
        logger = self._logger
        if kwargs.pop("exc_info", False):
            logger = logger.trace("error")
        if not isinstance(level, levels.LogLevel):
            raise ValueError("Unknown level: {0}".format(level))
        logger._emit(level, format_spec, args, kwargs)

root = FakeLogger(log.options(style="percent"))

_logger_cache = {} # name to logger
def getLogger(name=None):
    if name is not None:
        if name not in _logger_cache:
            _logger_cache[name] = FakeLogger(log.name(name).options(style="percent"))
        return _logger_cache[name]
    return root

