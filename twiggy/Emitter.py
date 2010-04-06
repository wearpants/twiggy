import time
import sys
import re

from .lib import ConversionTable, Converter

def msgFilter(x):
    if isinstance(x, bool):
        return lambda msg: x
    elif isinstance(x, basestring):
        return regex_wrapper(re.compile(x))
    elif isinstance(x, re.RegexObject):
        return regex_wrapper(x)
    elif callable(x): # XXX test w/ inspect.getargs here?
        return x
    else:
        # XXX a dict could be used to filter on fields (w/ callables?)
        raise ValueError("Unknown filter: {0!r}".format(x))

def regex_wrapper(regexp):
    assert isinstance(regexp, re.RegexObject)
    def wrapped(msg):
        return regexp.match(msg.text) is not None
    return wrapped


class Outputter(object):

    def __init__(self, format, write):
        self._format = format
        self._write = write

    def output(self, msg):
        x = self._format(msg)
        self._write(x)


class Emitter2(object):

    def __init__(self, min_level, filter, format, write):
        self.min_level = min_level
        self.filter = filter
        self._outputter = Outputter(format, write)

    def emit(self, msg):
        if self.filter(msg):
            self._outputter.output(msg)

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, f):
        self._filter = msgFilter(f)

    @filter.deleter
    def filter(self):
        del self._filter


class Emitter(object):
    """
    Emits!

    :ivar min_level: only emit if greater than this
    :type min_level: Levels.LogLevel
    """
    # XXX ABC me?
    def __init__(self, min_level):
        self.min_level = min_level

    def filter(self, msg):
        """return True if the message should be emitted

        I could be <some_regex>.match, perhaps
        """
        return True

    def format(self, msg):
        """
        :returns: the formatted message, ready for output
        :rtype: string
        """
        raise NotImplementedError

    def output(self, msg, s):
        """write out the message"""
        raise NotImplementedError

    def emit(self, msg):
        """emit a message.

        This is the only external API
        """
        if self.filter(msg):
            s = self.format(msg)
            self.output(msg, s)

class LineFormatter(object):

    def __init__(self, separator=':', traceback_prefix='\nTRACE ',
                 conversion=None, **kwargs):
        """
        Interesting trick:
        Setting traceback_prefix to '\\n' rolls it up to a single line.

        :ivar conversion: helper to turn a message to a string
        :type conversion: ConversionTable

        """
        self.separator = separator
        self.traceback_prefix = traceback_prefix

        if conversion is not None:
            self.conversion = conversion
        else:
            # XXX move this def out of init
            self.conversion = ConversionTable([
                Converter(key='time',
                          # ISO 8601 - it sucks less!
                          convertValue=lambda gmtime: time.strftime("%Y-%m-%dT%H:%M:%S", gmtime),
                          convertItem='{1}'.format,
                          required=True),
                Converter('level', str, '{1}'.format, True),
                Converter('name', str, '{1}'.format),
            ])

            self.conversion.genericValue = str
            self.conversion.genericItem = "{0}={1}".format
            self.conversion.aggregate = self.separator.join

    def format(self, msg):
        fields = self.format_fields(msg)
        text = self.format_text(msg)
        trace = self.format_traceback(msg)
        return "{fields}{self.separator}{text}{trace}".format(**locals()) # XXX gross?

    def format_text(self, msg):
        if msg.suppress_newlines:
            return msg.text.replace('\n', '\\n')
        else:
            return msg.text

    def format_traceback(self, msg):
        if msg.traceback is not None:
            # XXX this could be faster
            l = msg.traceback.split('\n')
            l = [""] + l[:-1]
            return self.traceback_prefix.join(l)
        else:
            return ""

    def format_fields(self, msg):
        return self.conversion.convert(msg.fields)

def printer(s):
    print>>sys.stderr, s