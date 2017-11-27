"""
Levels include (increasing severity): ``DEBUG``, ``INFO``, ``NOTICE``, ``WARNING``, ``ERROR``,
``CRITICAL``, ``DISABLED``
"""

from six import PY3, with_metaclass


class LogLevelMeta(type):
    """
    Metaclass that aids in making comparisons work the same in Python2 and Python3

    Python3 raises TypeError when unorderable types are compared via lt, gt, le, ge.
    Python2 picks an order but it doesn't always make much sense.

    In Python3, we only need the rich comparison operators to get this behaviour.

    In Python2, we use the __cmp__ function to raise TypeError for lt, gt, le, and ge.
    We define __eq__ and __ne__ on their own since those should just say that a LogLevel is never
    equal to a non-LogLevel.
    """
    def __new__(meta, name, bases, dct):
        cls = super(LogLevelMeta, meta).__new__(meta, name, bases, dct)

        if PY3:  # pragma: no py2 cover
            cls.__lt__ = cls._lt
            cls.__gt__ = cls._gt
            cls.__le__ = cls._le
            cls.__ge__ = cls._ge
            del cls.__cmp__
        else:  # pragma: no py3 cover
            del cls._lt
            del cls._gt
            del cls._le
            del cls._ge

        return cls


class LogLevel(with_metaclass(LogLevelMeta, object)):
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
        return "<LogLevel %s>" % self.__name

    def _lt(self, other):  # pragma: no py2 cover
        if not isinstance(other, LogLevel):
            return NotImplemented
        else:
            return self.__value < other.__value

    def _le(self, other):  # pragma: no py2 cover
        if not isinstance(other, LogLevel):
            return NotImplemented
        else:
            return self.__value <= other.__value

    def _gt(self, other):  # pragma: no py2 cover
        if not isinstance(other, LogLevel):
            return NotImplemented
        else:
            return self.__value > other.__value

    def _ge(self, other):  # pragma: no py2 cover
        if not isinstance(other, LogLevel):
            return NotImplemented
        else:
            return self.__value >= other.__value

    def __eq__(self, other):
        if not isinstance(other, LogLevel):
            return False
        else:
            return self.__value == other.__value

    def __ne__(self, other):
        if not isinstance(other, LogLevel):
            return True
        else:
            return self.__value != other.__value

    def __cmp__(self, other):  # pragma: no py3 cover
        # Python 2 only
        if not isinstance(other, LogLevel):
            raise TypeError('Unorderable types LogLevel() and %s' % type(other))
        elif self.__value < other.__value:
            return -1
        elif self.__value > other.__value:
            return 1
        else:
            return 0

    def __hash__(self):
        return hash(self.__value)


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
