"""
Loggers!
===========

"""

from .Message import Message
from .lib import iso8601time
import twiggy as _twiggy
import levels
import outputs
import formats

import sys
import time
import traceback
from functools import wraps

def emit(level):
    """a decorator that emits at ``level`` after calling the method. The method
    should return a Logger instance.

    For convenience, decorators for the various levels are available as
    ``emit.debug``, ``emit.info``, etc..

    """
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            f(self, *args, **kwargs)._emit(level)
        return wrapper
    return decorator

emit.debug = emit(levels.DEBUG)
emit.info = emit(levels.INFO)
emit.warning = emit(levels.WARNING)
emit.error = emit(levels.ERROR)
emit.critical = emit(levels.CRITICAL)

class BaseLogger(object):
    __slots__ = ['_fields', '_options', 'min_level']

    __valid_options = set(Message._default_options)

    def __init__(self, fields = None, options = None, min_level = None):
        """Constructor for internal module use only, basically.

        ``fields`` and ``options`` will be copied.
        """
        self._fields = fields.copy() if fields is not None else {}
        self._options = options.copy() if options is not None else Message._default_options.copy()
        self.min_level = min_level if min_level is not None else levels.DEBUG

    def _clone(self):
        return self.__class__(self._fields, self._options, self.min_level)

    def _emit(self):
        raise NotImplementedError

    ## The Magic
    def fields(self, **kwargs):
        clone = self._clone()
        clone._fields.update(kwargs)
        return clone

    def options(self, **kwargs):
        bad_options = set(kwargs) - self.__valid_options
        if bad_options:
            raise ValueError("Invalid options {0!r}".format(tuple(bad_options)))
        clone = self._clone()
        clone._options.update(kwargs)
        return clone

    ##  Convenience
    def trace(self, trace='error'):
        """enable tracing

        XXX write me!
        """
        return self.options(trace=trace)

    def name(self, name):
        return self.fields(name=name)

    ## Do something
    def debug(self, *args, **kwargs):
        self._emit(levels.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self._emit(levels.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self._emit(levels.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._emit(levels.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self._emit(levels.CRITICAL, *args, **kwargs)

class InternalLogger(BaseLogger):
    """
    :ivar output: an outputtter to write to
    :type output: Output
    """

    __slots__ = ['output']


    def __init__(self, fields = None, options = None, min_level = None, output = None):
        super(InternalLogger, self).__init__(fields, options)
        # XXX clobber this assert and make output mandatory?
        assert output is not None
        self.output = output

    def _clone(self):
        return self.__class__(self._fields, self._options, self.min_level, self.output)

    def _emit(self, level, format_spec = '',  *args, **kwargs):
        if level < self.min_level: return
        try:
            try:
                msg = Message(level, format_spec, self._fields.copy(), self._options.copy(), *args, **kwargs)
            except StandardError:
                msg = None
                raise
            else:
                self.output.output(msg)
        except StandardError:
            print>>sys.stderr, iso8601time(), "Error in twiggy internal log! Something is serioulsy broken."
            print>>sys.stderr, "Offending message:", repr(msg)
            traceback.print_exc(file = sys.stderr)

class Logger(BaseLogger):
    """
    :ivar filter: .. function:: filter(msg) -> bool
    """

    __slots__ = ['_emitters', 'filter']

    @classmethod
    def addFeature(cls, func, name=None):
        name = name if name is not None else func.__name__
        setattr(cls, name, func)

    @classmethod
    def disableFeature(cls, name):
        # get func directly from class dict - we don't want an unbound method.
        setattr(cls, name, cls.__dict__['clone'])

    @classmethod
    def delFeature(cls, name):
        delattr(cls, name)

    def __init__(self, fields = None, options = None, emitters = None,
                 min_level = None, filter = None):
        super(Logger, self).__init__(fields, options, min_level)
        self._emitters = emitters if emitters is not None else {}
        self.filter = filter if filter is not None else lambda format_spec: True

    def _clone(self):
        """return a new Logger instance with copied attributes

        Probably only for internal use.
        """
        return self.__class__(self._fields, self._options,
                              self._emitters, self.min_level, self.filter)

    @emit.info
    def struct(self, **kwargs):
        return self.fields(**kwargs)

    ## Boring stuff
    def _emit(self, level, format_spec = '',  *args, **kwargs):
        # XXX should these traps be collapsed?
        if level < self.min_level: return

        try:
            if not self.filter(format_spec): return
        except StandardError:
            _twiggy.internal_log.trace().info("Error in Logger filtering with {0!r} on {1}", self.filter, format_spec)
            # just continue emitting in face of filter error

        # XXX should we trap here too b/c of "Dictionary changed size during iteration" (or other rare errors?)
        potential_emitters = [(name, emitter) for name, emitter in self._emitters.iteritems()
                              if level >= emitter.min_level]

        if not potential_emitters: return

        try:
            msg = Message(level, format_spec, self._fields.copy(), self._options.copy(), *args, **kwargs)
        except StandardError:
            _twiggy.internal_log.trace().info("Error formatting message level: {0!r}, format: {1!r}, fields: {2!r}, "\
                                      "options: {3!r}, args: {4!r}, kwargs: {5!r}",
                                      level, format_spec, self._fields, self._options, args, kwargs)
            return

        outputs = set()
        for name, emitter in potential_emitters:
            try:
                include = emitter.filter(msg)
            except StandardError:
                _twiggy.internal_log.trace().info("Error filtering with emitter {0}. Message: {1!r}", name, msg)
            else:
                if include: outputs.add(emitter._output)

        for o in outputs:
            try:
                o.output(msg)
            except StandardError:
                _twiggy.internal_log.warning("Error outputting with {0!r}. Message: {1!r}", o, msg)

