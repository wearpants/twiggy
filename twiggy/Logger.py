import time

from Message import Message
import Levels

emitters = {}

def handle(msg):
    for emitter in emitters.itervalues():
        if emitter.level >= msg.level:
            # XXX add appropriate error trapping & logging; watch for recursion
            emitter.handle(msg)

class Logger(object):
    __slots__ = ['_fields']
    def __init__(self, fields = None):
        self._fields = fields if fields is not None else {}

    def fields(self, **kwargs):
        new_fields = self._fields.copy().update(**kwargs)
        return self.__class__(new_fields)

    def _handle(self, level, format_spec = '',  *args, **kwargs):
        handle(Message(level, format_spec, self._fields.copy(), *args, **kwargs))

    def name(self, name):
        return self.fields(name=name)

    def struct(self, **kwargs):
        self.fields(**kwargs).info()

    def debug(self, *args, **kwargs):
        self._handle(Levels.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self._handle(Levels.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self._handle(Levels.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._handle(Levels.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self._handle(Levels.CRITICAL, *args, **kwargs)

log = Logger({'time':time.time})