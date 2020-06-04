import fnmatch
import re

from six import string_types

from . import levels

__re_type = type(re.compile('foo'))  # XXX is there a canonical place for this?


def msg_filter(x):
    """intelligently create a filter"""
    # XXX replace lambdas with nicely-named functions, for debugging
    if x is None:
        return lambda msg: True
    elif isinstance(x, bool):
        return lambda msg: x
    elif isinstance(x, string_types):
        return regex_wrapper(re.compile(x))
    elif isinstance(x, __re_type):
        return regex_wrapper(x)
    elif callable(x):  # XXX test w/ inspect.getargs here?
        return x
    elif isinstance(x, (list, tuple)):
        return list_wrapper(x)
    else:
        # XXX a dict could be used to filter on fields (w/ callables?)
        raise ValueError("Unknown filter: {0!r}".format(x))


def list_wrapper(lst):
    filts = [msg_filter(i) for i in lst]

    def wrapped(msg):
        return all(f(msg) for f in filts)
    return wrapped


def regex_wrapper(regexp):
    assert isinstance(regexp, __re_type)

    def wrapped(msg):
        return regexp.match(msg.text) is not None
    return wrapped


def names(*names):
    """
    Returns a filter which matches message names against exact strings

    :args names: Any number of arguments are accepted.  Each one should be a string which can
        exactly match a message's name.
    :returns: A filter function.  The function returns True if the msg name is the same as one of
        the names provided here.
    """
    names_set = set(names)

    def set_names_filter(msg):
        return msg.name in names_set
    set_names_filter.names = names
    return set_names_filter


def glob_names(*names):
    """
    Return a filter which matches message names based on a list of globs

    :args names: Any number of arguments are accepted.  Each one should be a glob pattern which can
        match a message's name.
    :returns: A filter function.  The function returns True if the msg name matches one of the glob
        patterns provided here.
    """
    # copied from fnmatch.fnmatchcase - for speed
    patterns = [re.compile(fnmatch.translate(pat)) for pat in names]

    def glob_names_filter(msg):
        return any(pat.match(msg.name) is not None for pat in patterns)
    glob_names_filter.names = names
    return glob_names_filter


class Emitter(object):
    """Hold and manage an Output and associated filter."""

    def __init__(self, min_level, filter, output):
        if not isinstance(min_level, levels.LogLevel):
            raise ValueError("Unknown min_level: {0}".format(min_level))

        self.min_level = min_level
        self.filter = filter
        self._output = output

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, f):
        self._filter = msg_filter(f)
