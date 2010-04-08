import time
import sys
import re

from .lib import ConversionTable, Converter

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
    """
    Does the work of formatting and writing a message.

    Multiple implementations are expected.

    format(msg) -> <whatever>
    format the message for writing. Output type is user-specified, as long as
    it's compatible with write()

    write(<whatever>) -> None
    writes out the formatted message

    """

    def __init__(self, format, write):
        self._format = format
        self._write = write

    def output(self, msg):
        x = self._format(msg)
        self._write(x)

    # XXX I prolly need a close() or somesuch

class Emitter(object):
    """
    Emits!

    :ivar min_level: only emit if greater than this
    :type min_level: Levels.LogLevel

    filter(msg) -> bool
    should the message be emitted

    """

    def __init__(self, min_level, filter, format, write, outputter=Outputter):
        self.min_level = min_level
        self.filter = filter
        self._outputter = outputter(format, write)

    def emit(self, msg):
        """emit a message.

        This is the only external API
        """
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

    # XXX I prolly need a close() or somesuch

# a default converter
line_conversion = ConversionTable([
    Converter(key='time',
              # ISO 8601 - it sucks less!
              convertValue=lambda gmtime: time.strftime("%Y-%m-%dT%H:%M:%S", gmtime),
              convertItem='{1}'.format,
              required=True),
    ('level', str, '{1}'.format, True),
    ('name', str, '{1}'.format),
])

line_conversion.genericValue = str
line_conversion.genericItem = "{0}={1}".format
line_conversion.aggregate = ':'.join

class LineFormatter(object):
    """format a message for text-oriented output"""

    def __init__(self, separator=':', traceback_prefix='\nTRACE ',
                 conversion=line_conversion, **kwargs):
        """
        Interesting trick:
        Setting traceback_prefix to '\\n' rolls it up to a single line.

        :ivar conversion: helper to turn a message to a string
        :type conversion: ConversionTable

        """
        self.separator = separator
        self.traceback_prefix = traceback_prefix
        self.conversion = conversion

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