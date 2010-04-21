import Levels

import re

__re_type = type(re.compile('foo')) # XXX is there a canonical place for this?

def msgFilter(x):
    """return a function suitable for use as a filter with emitters.

    You may pass:

    :None, True: the filter will always return True
    :False: the filter will always return False
    :string: compiled into a regex
    :regex: match()ed against the message text
    :callable: returned as is

    """
    if x is None:
        return lambda msg: True
    elif isinstance(x, bool):
        return lambda msg: x
    elif isinstance(x, basestring):
        return regex_wrapper(re.compile(x))
    elif isinstance(x, __re_type):
        return regex_wrapper(x)
    elif callable(x): # XXX test w/ inspect.getargs here?
        return x
    else:
        # XXX a dict could be used to filter on fields (w/ callables?)
        raise ValueError("Unknown filter: {0!r}".format(x))

def regex_wrapper(regexp):
    assert isinstance(regexp, __re_type)
    def wrapped(msg):
        return regexp.match(msg.text) is not None
    return wrapped

class Emitter(object):
    """
    Emits!

    :ivar min_level: only emit if greater than this
    :type min_level: Levels.LogLevel

    filter(msg) -> bool
    should the message be emitted

    """

    def __init__(self, min_level, filter, outputter):
        if not isinstance(min_level, Levels.LogLevel):
            raise ValueError("Unknown min_level: {0}".format(min_level))

        self.min_level = min_level
        self.filter = filter
        self._outputter = outputter

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, f):
        self._filter = msgFilter(f)

    @filter.deleter
    def filter(self):
        del self._filter

    # XXX I prolly need a close() or somesuch