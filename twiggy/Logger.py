from Message import Message
import Levels

class Logger(object):
    __slots__ = ['_fields', 'emitters', 'min_level']

    def __init__(self, fields = None, emitters = None, min_level = Levels.DEBUG):
        self._fields = fields if fields is not None else {}
        self.emitters = emitters if emitters is not None else {}
        self.min_level = min_level

    def fields(self, **kwargs):
        new_fields = self._fields.copy()
        new_fields.update(**kwargs)
        return self.__class__(new_fields, self.emitters, self.min_level)

    def name(self, name):
        return self.fields(name=name)

    def struct(self, **kwargs):
        self.fields(**kwargs).info()

    def _emit(self, level, format_spec = '',  *args, **kwargs):
        if level < self.min_level: return

        msg = Message(level, format_spec, self._fields.copy(), *args, **kwargs)

        for emitter in self.emitters.itervalues():
            if emitter.min_level >= msg.level:
                # XXX add appropriate error trapping & logging; watch for recursion
                emitter.emit(msg)

    def debug(self, *args, **kwargs):
        self._emit(Levels.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self._emit(Levels.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self._emit(Levels.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._emit(Levels.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self._emit(Levels.CRITICAL, *args, **kwargs)