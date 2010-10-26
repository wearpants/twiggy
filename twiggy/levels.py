"""
Levels include (increasing severity): ``DEBUG``, ``INFO``, ``NOTICE``, ``WARNING``, ``ERROR``, ``CRITICAL``, ``DISABLED``
"""

class LogLevel(object):
    """A log level. Users should *not* create new instances.

    Levels are opaque; they may be compared to each other, but nothing else.
    """

    __slots__ = ['__name', '__value']
    _name2levels = {}

    def __init__(self, name, value):
        self.__name = name
        self.__value = value
        self._name2levels[name] = self

    def __str__(self):
        return self.__name

    def __repr__(self):
        return "<LogLevel %s>"%self.__name

    def __cmp__(self, other):
        if not isinstance(other, LogLevel):
            return NotImplemented
        else:
            return cmp(self.__value, other.__value)

def name2level(name):
    """return a `LogLevel` from a case-insensitve string"""
    return LogLevel._name2levels[name.upper()]

DEBUG = LogLevel('DEBUG', 1)
INFO = LogLevel('INFO', 2)
NOTICE = LogLevel('NOTICE', 3)
WARNING = LogLevel('WARNING', 4)
ERROR = LogLevel('ERROR', 5)
CRITICAL = LogLevel('CRITICAL', 6)
DISABLED = LogLevel('DISABLED', 7)
