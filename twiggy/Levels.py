__all__ = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

class LogLevel(object):
    __slots__ = ['__name,', '__value']
    levels = {}

    def __init__(self, name, value):
        self.__name = name
        self.__value = value
        self.levels[name] = self

    def __str__(self):
        return self.__name

    def __repr__(self):
        return "<LogLevel %s>"%self.__name

    def __cmp__(self, other):
        return cmp(self.__value, other.__value)

DEBUG = LogLevel('DEBUG', 1)
INFO = LogLevel('INFO', 2)
WARNING = LogLevel('WARNING', 3)
ERROR = LogLevel('ERROR', 4)
CRITICAL = LogLevel('CRITICAL', 5)