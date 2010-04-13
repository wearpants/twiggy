from Message import Message
import Levels

class Logger(object):
    """
    :ivar min_level: only emit if message level is above this
    :type min_level: Levels.LogLevel

    :ivar filter: ..function:: filter(msg) -> bool
    """
    __slots__ = ['_fields', '_options', 'emitters', 'min_level', 'filter']

    __valid_options = set(Message._default_options)

    def __init__(self, fields = None, options = None, emitters = None,
                 min_level = Levels.DEBUG, filter = None):
        """Constructor for internal module use only, basically."""
        self._fields = fields if fields is not None else {}
        self._options = options if options is not None else Message._default_options.copy()
        self.emitters = emitters if emitters is not None else {}
        self.min_level = min_level
        self.filter = filter if filter is not None else lambda format_spec: True

    def fields(self, **kwargs):
        new_fields = self._fields.copy()
        new_fields.update(**kwargs)
        return self.__class__(new_fields, self._options.copy(),
                              self.emitters, self.min_level, self.filter)

    def options(self, **kwargs):
        new_options = self._options.copy()
        new_options.update(**kwargs)
        bad_options = set(kwargs) - self.__valid_options
        if bad_options:
            raise ValueError("Invalid options {0!r}".format(tuple(bad_options)))
        return self.__class__(self._fields.copy(), new_options,
                              self.emitters, self.min_level, self.filter)

    ##  Convenience
    def trace(self, trace='error'):
        return self.options(trace=trace)

    def name(self, name):
        return self.fields(name=name)

    def struct(self, **kwargs):
        self.fields(**kwargs).info()

    ## Boring stuff

    def _emit(self, level, format_spec = '',  *args, **kwargs):
        if (level < self.min_level or not self.filter(format_spec)): return

        potential_emitters = [(name, emitter) for name, emitter in self.emitters.iteritems()
                              if level >= emitter.min_level]

        if not potential_emitters: return

        msg = Message(level, format_spec, self._fields.copy(), self._options, *args, **kwargs)

        # XXX add appropriate error trapping & logging; watch for recursion
        # don't forget to trap errors from filter!
        for o in set(e.outputter for n, e in potential_emitters if e.filter(msg)):
            o.output(msg)

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